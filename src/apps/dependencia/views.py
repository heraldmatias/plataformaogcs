# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, redirect
from forms import MinisterioForm, OdpForm, GobernacionForm, ConsultaMinisterioForm,ConsultaOdpForm,ConsultaGobernacionForm, MinisterioTable,OdpTable,GobernacionTable
from django.template import RequestContext
from usuario.models import Usuario, Estado
from models import Ministerio, Odp, Gobernacion
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
import django_tables2 as tables
from django_tables2.config import RequestConfig
from ubigeo.models import Provincia
from django.db.models import Q
from datetime import datetime
from scripts.scripts import imprimirToExcel

@login_required(login_url='/')
def ministerioadd(request):
    profile = Usuario.objects.get(user = request.user)
    if request.method == 'POST':
        num = Ministerio.objects.values("nummin").order_by("-nummin",)[:1]
        num = 1 if len(num)==0 else int(num[0]["nummin"])+1
        iministerio = Ministerio(nummin=num,estado=Estado.objects.get(pk=1),idusuario_creac=profile.numero)
        frmministerio = MinisterioForm(request.POST, instance=iministerio) # A form bound to the POST data
        if frmministerio.is_valid():
            frmministerio.save()
            return redirect('/home/') # Crear un parametro en home para mostrar los mensajes de exito.
    else:        
        frmministerio = MinisterioForm()
    return render_to_response('dependencia/ministerio.html', {'frmministerio': frmministerio,'opcion':'add','usuario':request.session['nombres'],'fecha':request.session['login_date']}, context_instance=RequestContext(request),)

@login_required(login_url='/')
def ministerioedit(request, codigo):
    if request.method == 'POST':
        profile = Usuario.objects.get(user = request.user)
        ministerio = Ministerio.objects.get(nummin=int(codigo))
        ministerio.idusuario_mod=profile.numero
        frmministerio = MinisterioForm(request.POST, instance=ministerio) # A form bound to the POST data	
        if frmministerio.is_valid():
            frmministerio.save()
            return redirect('/home/') # Crear un parametro en home para mostrar los mensajes de exito.
    else:
        ministerio = get_object_or_404(Ministerio, nummin=int(codigo))
        frmministerio = MinisterioForm(instance=ministerio)
    return render_to_response('dependencia/ministerio.html', {'frmministerio': frmministerio,'opcion':'edit','codigo':codigo,'usuario':request.session['nombres'],'fecha':request.session['login_date']}, context_instance=RequestContext(request),)

@login_required(login_url='/')
def ministerioquery(request):
    col = "-ministerio"
    if "2-sort" in request.GET:
        col = request.GET['2-sort']
    config = RequestConfig(request)
    consultaministerioform = ConsultaMinisterioForm(request.GET)
    if 'ministerio' in request.GET:
        ministerios = Ministerio.objects.filter(ministerio__icontains=request.GET['ministerio']).order_by(col)
    else:
        ministerios = Ministerio.objects.all().order_by(col)
    tblministerios = MinisterioTable(ministerios.order_by(col))
    config.configure(tblministerios)
    tblministerios.paginate(page=request.GET.get('page', 1), per_page=6)
    return render_to_response('dependencia/ministerio_consulta.html', {'consultaministerioform':consultaministerioform,'tabla':tblministerios,'usuario':request.session['nombres'],'fecha':request.session['login_date']}, context_instance=RequestContext(request),)

@login_required(login_url='/')
def ministerioprint(request):
    col = 'ministerio'
    if 'ministerio' in request.GET:
        query = Ministerio.objects.filter(ministerio__icontains=request.GET['ministerio']).order_by(col)
    else:
        query = Ministerio.objects.all().order_by(col)
    filename= "ministerio_%s.xls" % datetime.today().strftime("%Y%m%d")
    return imprimirToExcel('dependencia/reportemin.html', {'data': query,'fecha':datetime.today().date(),'hora':datetime.today().time(),'usuario':request.session['nombres']},filename)

@login_required(login_url='/')
def odpadd(request):
    profile = Usuario.objects.get(user = request.user)
    if request.method == 'POST':
        num = Odp.objects.values("numodp").order_by("-numodp",)[:1]
        num = 1 if len(num)==0 else int(num[0]["numodp"])+1
        iodp = Odp(numodp=num,estado=Estado.objects.get(pk=1),idusuario_creac=profile.numero)
        frmopd = OdpForm(request.POST, instance=iodp) # A form bound to the POST data
        if frmopd.is_valid():
            frmopd.save()
            return redirect('/home/') # Crear un parametro en home para mostrar los mensajes de exito.
    else:        
        frmopd = OdpForm()
    return render_to_response('dependencia/odp.html', {'frmodp': frmopd,'opcion':'add','usuario':request.session['nombres'],'fecha':request.session['login_date']}, context_instance=RequestContext(request),)

@login_required(login_url='/')
def odpedit(request, codigo):
    if request.method == 'POST':
        profile = Usuario.objects.get(user = request.user)
        odp = Odp.objects.get(numodp=int(codigo))
        odp.idusuario_mod=profile.numero
        frmodp = OdpForm(request.POST, instance=odp) # A form bound to the POST data	
        if frmodp.is_valid():
            frmodp.save()
            return redirect('/home/') # Crear un parametro en home para mostrar los mensajes de exito.
    else:
        odp = get_object_or_404(Odp, numodp=int(codigo))
        frmodp = OdpForm(instance=odp)
    return render_to_response('dependencia/odp.html', {'frmodp': frmodp,'opcion':'edit','codigo':codigo,'usuario':request.session['nombres'],'fecha':request.session['login_date']}, context_instance=RequestContext(request),)

@login_required(login_url='/')
def odpquery(request):
    col = "-odp"
    if "2-sort" in request.GET:
        col = request.GET['2-sort']    
    config = RequestConfig(request)
    consultaodpform = ConsultaOdpForm(request.GET)
    if 'nummin' in request.GET and 'odp' in request.GET:   
       if (request.GET['nummin'] and request.GET['odp']) or request.GET['nummin']:
          odps = Odp.objects.filter(odp__icontains=request.GET['odp'],nummin=request.GET['nummin']).order_by(col)
       elif request.GET['odp']:
          odps = Odp.objects.filter(odp__icontains=request.GET['odp']).order_by(col)
       else:
          odps = Odp.objects.all()
    else:
       odps = Odp.objects.all()
    tblodps = OdpTable(odps.order_by(col))
    config.configure(tblodps)
    tblodps.paginate(page=request.GET.get('page', 1), per_page=6)
    return render_to_response('dependencia/odp_consulta.html', {'consultaodpform':consultaodpform,'tabla':tblodps,'usuario':request.session['nombres'],'fecha':request.session['login_date']}, context_instance=RequestContext(request),)

@login_required(login_url='/')
def odpprint(request):
    col = 'odp'
    if (request.GET['nummin'] and request.GET['odp']) or request.GET['nummin']:
        query = Odp.objects.filter(odp__icontains=request.GET['odp'],nummin=request.POST['nummin']).order_by(col)
    elif request.GET['odp']:
        query = Odp.objects.filter(odp__icontains=request.GET['odp']).order_by(col)
    else:
        query = Odp.objects.all().order_by(col)
    filename= "odp_%s.xls" % datetime.today().strftime("%Y%m%d")
    return imprimirToExcel('dependencia/reporteodp.html', {'data': query,'fecha':datetime.today().date(),'hora':datetime.today().time(),'usuario':request.session['nombres']},filename)

@login_required(login_url='/')
def gobernacionadd(request):
    profile = Usuario.objects.get(user = request.user)
    if request.method == 'POST':
        from ubigeo.models import Region
        num = Gobernacion.objects.values("numgob").order_by("-numgob",)[:1]
        num = 1 if len(num)==0 else int(num[0]["numgob"])+1
        region = Region()
        if request.POST['region']:
            region = Region.objects.get(numreg= request.POST['region'])
        igobernacion = Gobernacion(numgob=num,estado=Estado.objects.get(pk=1),region= region,idusuario_creac=profile.numero)
        frmgobernacion = GobernacionForm(request.POST, instance=igobernacion) # A form bound to the POST data
        if frmgobernacion.is_valid():
            frmgobernacion.save()
            return redirect('/home/') # Crear un parametro en home para mostrar los mensajes de exito.
    else:        
        frmgobernacion = GobernacionForm()
    return render_to_response('dependencia/gobernacion.html', {'frmgobernacion': frmgobernacion,'opcion':'add','usuario':request.session['nombres'],'fecha':request.session['login_date']}, context_instance=RequestContext(request),)

@login_required(login_url='/')
def gobernacionedit(request, codigo):
    if request.method == 'POST':
        profile = Usuario.objects.get(user = request.user)
        gobernacion = Gobernacion.objects.get(numgob=int(codigo))
        gobernacion.idusuario_mod=profile.numero
        frmgobernacion = GobernacionForm(request.POST, instance=gobernacion) # A form bound to the POST data	
        if frmgobernacion.is_valid():
            frmgobernacion.save()
            return redirect('/home/') # Crear un parametro en home para mostrar los mensajes de exito.
    else:
        gobernacion = get_object_or_404(Gobernacion, numgob=int(codigo))
        frmgobernacion = GobernacionForm(instance=gobernacion)
        #frmgobernacion.provincia.choices = Provincia.objects.filter(region=gobernacion.region).values_list('numpro','provincia')        
    return render_to_response('dependencia/gobernacion.html', {'frmgobernacion': frmgobernacion,'opcion':'edit','codigo':codigo,'usuario':request.session['nombres'],'fecha':request.session['login_date']}, context_instance=RequestContext(request),)

@login_required(login_url='/')
def gobernacionquery(request):
    col = "-gobernacion"
    if "2-sort" in request.GET:
        col = request.GET['2-sort']
    config = RequestConfig(request)
    consultagobernacionform = ConsultaGobernacionForm(request.GET)
    print consultagobernacionform
    if 'region' in request.GET and 'provincia' in request.GET:
	if request.GET['region'] and request.GET['provincia']:
	    gobernaciones = Gobernacion.objects.filter(region=request.GET['region'], provincia=request.GET['provincia']).order_by(col)
	elif request.GET['region']:
	    gobernaciones = Gobernacion.objects.filter(region=request.GET['region'],).order_by(col)
        else:
	    gobernaciones = Gobernacion.objects.all().order_by(col)
    else:
        gobernaciones = Gobernacion.objects.all().order_by(col)
    tblgobernaciones = GobernacionTable(gobernaciones.order_by(col))
    config.configure(tblgobernaciones)
    tblgobernaciones.paginate(page=request.GET.get('page', 1), per_page=6)
    return render_to_response('dependencia/gobernacion_consulta.html', {'consultagobernacionform':consultagobernacionform,'tabla':tblgobernaciones,'usuario':request.session['nombres'],'fecha':request.session['login_date']}, context_instance=RequestContext(request),)

@login_required(login_url='/')
def gobernacionprint(request):
    col = 'gobernacion'
    if (request.GET['region'] and request.GET['provincia']) or request.GET['region']:
        query = Gobernacion.objects.filter(region=request.GET['region'], provincia=request.GET['provincia']).order_by(col)
    elif request.GET['provincia']:
        query = Gobernacion.objects.filter(provincia=request.GET['region']).order_by(col)
    else:
        query = Gobernacion.objects.all().order_by(col)
    filename= "gobernacion_%s.csv" % datetime.today().strftime("%Y%m%d")
    return imprimirToExcel('dependencia/reportegob.html', {'data': query,'fecha':datetime.today().date(),'hora':datetime.today().time(),'usuario':request.session['nombres']},filename)

@login_required(login_url='/')
def jsondependencia(request):
    if not request.GET['r']:
        dependencia ={}
    elif int(request.GET['r'])==1:
        dependencia = Ministerio.objects.all().order_by('ministerio')
    elif int(request.GET['r'])==2:
        dependencia = Odp.objects.all().order_by('odp')
    elif int(request.GET['r'])==3:
        dependencia = Gobernacion.objects.all().order_by('gobernacion')
    return HttpResponse(serializers.serialize("json", dependencia, ensure_ascii=False),mimetype='application/json')

