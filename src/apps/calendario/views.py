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
    if request.method == 'POST':
        form = EventoForm(request.POST,error_class=DivErrorList, instance=evento)
        if form.is_valid():
            messages.add_message(request, messages.SUCCESS, 
                   'Registro %s exitosamente!' % ((codigo)and'Modificado'or'Grabado') )         
            if codigo:
                evento.idusuario_mod = request.user.get_profile()
                evento.fec_mod = datetime.today()
                evento.save()
                #insert_or_update_event(evento,url_edit)
                return redirect('ogcs-mantenimiento-evento-query') 
            else:
                evento = form.save(commit=False)
                evento.idusuario_creac = request.user.get_profile()
                evento.fec_creac = datetime.today()
                evento.organismo_id = evento.idusuario_creac.organismo_id
                evento.dependencia = evento.idusuario_creac.dependencia
                evento.save()
                #insert_or_update_event(evento)
            form = EventoForm()
    else:        
        form = EventoForm(instance = evento)
    return render_to_response('calendar/actividad.html',
                              {
                                  'form':form,
                                  'opcion':'add',
                                  'codigo':codigo,
                                  'evento': evento if evento else ''
                              }, context_instance=RequestContext(request))


def eventoquery(request):
    form = EventoConsultaForm(request.GET)
    usuario = request.user.get_profile()
    query = Evento.objects.all()
    if 'fechaini' in request.GET:
        start_date = None
        try:
            start_date = ((request.GET['fechaini']) and
                datetime.strptime(request.GET['fechaini'],"%d/%m/%Y") or None)
        except:
            pass
        if start_date:
            query = query.filter(fec_inicio=start_date)
        #if start_date and end_date:
        #    query = query.filter(fec_inicio__gte=start_date, fec_termin__lte= end_date)
        #elif start_date:
        #    query = query.filter(fec_inicio__gte=start_date)
        #elif end_date:
        #    query = query.filter(fec_termin__lte=end_date)
    if request.GET.get('titulo'):
        query = query.filter(titulo__icontains=request.GET.get('titulo'))
    if request.GET.get('organismo') and request.GET.get('dependencia'):
        query = query.filter(organismo__codigo = request.GET.get('organismo'), dependencia = request.GET.get('dependencia'))
    if request.GET.get('organismo'):
        query = query.filter(organismo__codigo = request.GET.get('organismo'))
    if request.GET.get('region') and request.GET.get('provincia') and request.GET.get('distrito'):
        query = query.filter(region = request.GET.get('region'), provincia = request.GET.get('provincia'), distrito = request.GET.get('distrito'))
    elif request.GET.get('region') and request.GET.get('provincia'):
        query = query.filter(region = request.GET.get('region'), provincia = request.GET.get('provincia'))
    elif request.GET.get('region'):
        query = query.filter(region = request.GET.get('region'))
    #query = query.filter(organismo__codigo = usuario.organismo_id,
    #	dependencia=usuario.dependencia)
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