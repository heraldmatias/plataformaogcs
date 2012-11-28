# Create your views here.
# -*- coding: utf-8 -*-
from django.contrib import messages
from calendar import insert_or_update_event, delete_calendar
from models import Evento
from forms import EventoForm, EventoTable, EventoConsultaForm
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from datetime import datetime
from django_tables2.config import RequestConfig
from scripts.scripts import DivErrorList
from django.utils import simplejson
from django.http import HttpResponse
def eventoadd(request, codigo=None):
    evento = None
    url_edit = None
    if codigo:
        evento = Evento.objects.get(pk=codigo)
        url_edit = evento.url_edit
    if request.method == 'POST':
        form = EventoForm(request.POST,error_class=DivErrorList,instance = evento)
        if form.is_valid():
            messages.add_message(request, messages.SUCCESS, 
                   'Registro %s exitosamente!' % ((codigo)and'Modificado'or'Grabado') )         
            if codigo:
                evento.idusuario_mod = request.user.get_profile()
                evento.fec_mod = datetime.today()                
                insert_or_update_event(evento,url_edit)                
                
                return redirect('ogcs-mantenimiento-evento-query') 
            else:
                evento = form.save(commit=False)
                evento.idusuario_creac = request.user.get_profile()
                evento.fec_creac = datetime.today()
                evento.organismo_id = evento.idusuario_creac.organismo_id
                evento.dependencia = evento.idusuario_creac.dependencia
                insert_or_update_event(evento)                
            form = EventoForm()
    else:        
        form = EventoForm(instance = evento)
    return render_to_response('calendar/actividad.html',{'form':form,
        'opcion':'add','codigo':codigo},context_instance=RequestContext(request))


def eventoquery(request):
    form = EventoConsultaForm(request.GET)
    usuario = request.user.get_profile()
    query = Evento.objects.all()
    if 'fechaini' in request.GET and 'fechafin' in request.GET:
        start_date = None
        end_date = None
        try:
            start_date = ((request.GET['fechaini']) and
                datetime.strptime(request.GET['fechaini'],"%d/%m/%Y") or None)
            end_date = ((request.GET['fechafin']) and
                datetime.strptime(request.GET['fechafin'],"%d/%m/%Y") or None)
        except:
            pass
        if start_date and end_date:
            query = query.filter(fec_inicio__gte=start_date, fec_termin__lte= end_date)
        elif start_date:
            query = query.filter(fec_inicio__gte=start_date)
        elif end_date:
            query = query.filter(fec_termin__lte=end_date)
    if request.GET.get('titulo'):
        query = query.filter(titulo__icontains=request.GET.get('titulo'))
    query = query.filter(organismo__codigo = usuario.organismo_id,
    	dependencia=usuario.dependencia)
    table_eventos = EventoTable(query)
    config = RequestConfig(request,paginate={"per_page": 10})
    config.configure(table_eventos)
    return render_to_response('calendar/consulta_actividad.html',
    	{'form':form,'table_eventos':table_eventos},context_instance=RequestContext(request))	

def eventodelete(request):
    results = {'success':False}
    if request.POST:        
        evento = Evento.objects.filter(pk=
            request.POST.get('codigo')).values_list('url_edit')
        if len(evento)>0:
            delete_calendar(evento[0][0])
            Evento.objects.filter(pk=request.POST.get('codigo')).delete()
            results = {'success':True}    
    json = simplejson.dumps(results)
    return HttpResponse(json, mimetype='application/json')