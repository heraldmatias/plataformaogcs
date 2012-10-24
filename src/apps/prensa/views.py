# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from models import ResumenPrensa, CasoExito
from forms import (ResumenPrensaForm, 
	CasoExitoForm, ConsultaRepForm, RepTable)
from datetime import datetime
from django.core.files.storage import  FileSystemStorage,default_storage
from scripts.scripts import imprimirToPDF, DivErrorList
from django.contrib import messages
from django_tables2.config import RequestConfig
from django.template.loader import render_to_string
from django.contrib.sites.models import get_current_site
@login_required()
def add_resumen_prensa(request, codigo=None):
    obj = None
    if codigo:
        obj = get_object_or_404(ResumenPrensa,pk=codigo)
    if request.method == 'POST':
    	if 'archivo' in request.FILES:
            profile = request.user.get_profile()
            ini=request.session['dependencia']
            filename1 = request.FILES['archivo'].name
            ext = filename1[filename1.rfind('.')+1:]
            filename= "REP%s%s.%s" % (ini.iniciales,
                datetime.strptime(request.POST['fecha'],"%d/%m/%Y").strftime("%d%m%Y"),ext)            
            if not obj:
                obj = ResumenPrensa(organismo=profile.organismo,
                    dependencia=profile.dependencia,idusuario_creac_id=profile.numero,)
            else:
                obj.idusuario_mod = profile
                obj.fec_mod = datetime.today()           
            request.FILES['archivo'].name = filename
            filename1 = obj.archivo
        formulario = ResumenPrensaForm(request.POST, request.FILES, instance= obj, error_class=DivErrorList)        
        if formulario.is_valid():
            if codigo and 'archivo' in request.FILES:
                FileSystemStorage().delete(filename1)
            formulario.save()            
            messages.add_message(request, messages.SUCCESS, 
               'Registro %s exitosamente!' % ((codigo)and'Modificado'or'Grabado') )
            if codigo:
                return redirect('ogcs-mantenimiento-prensa-rep-query')
            formulario = ResumenPrensaForm()
    else:
    	formulario = ResumenPrensaForm(instance= obj)    
    return render_to_response('prensa/rep.html', {'formulario': formulario,
        'resumen':((codigo) and obj or None)}, context_instance=RequestContext(request),)

@login_required()
def query_resumen_prensa(request):
    col = "-organismo"
    query = None
    dependencia=''    
    query = ResumenPrensa.objects.all()
    if "2-sort" in request.GET:
        col = request.GET['2-sort']
    config = RequestConfig(request)
    formulario = ConsultaRepForm(request.GET)
    if 'organismo' in request.GET:
        if request.GET['organismo']:            
            query = query.filter(organismo_id=request.GET['organismo'])
    if 'dependencia' in request.GET:
        if request.GET['dependencia']:            
            dependencia=request.GET['dependencia']
            query = query.filter(dependencia=request.GET['dependencia'])
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
            query = query.filter(fecha__range=(start_date, end_date))
        elif start_date:
            query = query.filter(fecha__gte=start_date)
        elif end_date:
            query = query.filter(fecha__lte=end_date)    
    query = query.extra(tables=
        ['usuario',],select={'usuario':'usuario.usuario',
        'dependencia':"""case tbl_resumen_prensa.organismo_id when 1
         then (select ministerio from ministerio where nummin=tbl_resumen_prensa.dependencia) 
         when 2 then (select odp from odp where numodp=tbl_resumen_prensa.dependencia) 
         when 3 then (select gobernacion from gobernacion 
            where numgob=tbl_resumen_prensa.dependencia) end"""})
    tabla = RepTable(query.order_by(col))
    config.configure(tabla)
    tabla.paginate(page=request.GET.get('page', 1), per_page=6)
    return render_to_response('prensa/rep_consulta.html', 
    	{'formulario':formulario,'tabla':tabla,'dependencia':dependencia,}, 
    	context_instance=RequestContext(request),)

@login_required
def print_resumen_prensa(request):
    col = "-organismo"
    query = None
    dependencia=''    
    query = ResumenPrensa.objects.all()
    if "2-sort" in request.GET:
        col = request.GET['2-sort']
    config = RequestConfig(request)
    formulario = ConsultaRepForm(request.GET)
    if 'organismo' in request.GET:
        if request.GET['organismo']:            
            query = query.filter(organismo_id=request.GET['organismo'])
    if 'dependencia' in request.GET:
        if request.GET['dependencia']:            
            dependencia=request.GET['dependencia']
            query = query.filter(dependencia=request.GET['dependencia'])
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
            query = query.filter(fecha__range=(start_date, end_date))
        elif start_date:
            query = query.filter(fecha__gte=start_date)
        elif end_date:
            query = query.filter(fecha__lte=end_date)    
    data = query.extra(select={'dependencia':"""case tbl_resumen_prensa.organismo_id when 1
         then (select ministerio from ministerio where nummin=tbl_resumen_prensa.dependencia) 
         when 2 then (select odp from odp where numodp=tbl_resumen_prensa.dependencia) 
         when 3 then (select gobernacion from gobernacion 
            where numgob=tbl_resumen_prensa.dependencia) end"""}).values('codigo',
    'idusuario_creac__nombres','idusuario_creac__apellidos','organismo__nombre',
    'fecha','dependencia','descripcion','archivo')    
    domain = get_current_site(request).domain
    html = render_to_string('prensa/rep_reporte.html',{'data': data,
        'protocol':request.is_secure() and 'https' or 'http',
        'pagesize':'A4','usuario':request.user.get_profile(),'domain':domain},
        context_instance=RequestContext(request))
    filename= "rep_%s.pdf" % datetime.today().strftime("%Y%m%d")        
    return imprimirToPDF(html,filename) 