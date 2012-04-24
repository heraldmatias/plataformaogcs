# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, redirect
from forms import RegionForm, ProvinciaForm, ConsultaRegionForm, RegionTable, ConsultaProvinciaForm, ProvinciaTable
from django.template import RequestContext
from usuario.models import Usuario, Estado
from models import Region, Provincia
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
import django_tables2 as tables
from django_tables2.config import RequestConfig

@login_required(login_url='/')
def regionadd(request):
    if request.method == 'POST':
        profile = Usuario.objects.get(user = request.user)
        num = Region.objects.values("numreg").order_by("-numreg",)[:1]
        num = 1 if len(num)==0 else int(num[0]["numreg"])+1
        region = Region(numreg=num,estado=Estado.objects.get(pk=1),idusuario_creac=profile.numero,)
        frmregion = RegionForm(request.POST, instance=region) # A form bound to the POST data
        if frmregion.is_valid():
            frmregion.save()
            return redirect('/home/') # Crear un parametro en home para mostrar los mensajes de exito.
    else:        
        frmregion = RegionForm()
    return render_to_response('ubigeo/region.html', {'frmregion': frmregion,'opcion':'add','usuario':request.session['nombres'],'fecha':request.session['login_date']}, context_instance=RequestContext(request),)

@login_required(login_url='/')
def regionedit(request, codigo):
    if request.method == 'POST':
        profile = Usuario.objects.get(user = request.user)
        region = Region.objects.get(numreg=int(codigo))
        region.idusuario_mod=profile.numero
        frmregion = RegionForm(request.POST, instance=region) # A form bound to the POST data	
        if frmregion.is_valid():
            frmregion.save()
            return redirect('/home/') # Crear un parametro en home para mostrar los mensajes de exito.
    else:
        region = get_object_or_404(Region, numreg=int(codigo))
        frmregion = RegionForm(instance=region)
    return render_to_response('ubigeo/region.html', {'frmregion': frmregion,'opcion':'edit','codigo':codigo,'usuario':request.session['nombres'],'fecha':request.session['login_date']}, context_instance=RequestContext(request),)

@login_required(login_url='/')
def regionquery(request):
    col = "-region"
    if "2-sort" in request.GET:
        col = request.GET['2-sort']
    regiones = Region.objects.all()
    config = RequestConfig(request)
    if request.method == "POST":
        consultaregionform = ConsultaRegionForm(request.POST)        
        if consultaregionform.is_valid():
            print consultaregionform
            regiones = regiones.filter(region__icontains=request.POST['region']).order_by(col)
    else:
        consultaregionform = ConsultaRegionForm()
    tblregiones = RegionTable(regiones.order_by(col))
    config.configure(tblregiones)
    tblregiones.paginate(page=request.GET.get('page', 1), per_page=6)
    return render_to_response('ubigeo/region_consulta.html', {'consultaregionform':consultaregionform,'tblregiones':tblregiones,'usuario':request.session['nombres'],'fecha':request.session['login_date']}, context_instance=RequestContext(request),)

@login_required(login_url='/')
def provinciaadd(request):
    profile = Usuario.objects.get(user = request.user)
    if request.method == 'POST':
        num = Provincia.objects.values("numpro").order_by("-numpro",)[:1]
        num = 1 if len(num)==0 else int(num[0]["numpro"])+1
        provincia = Provincia(numpro=num,estado=Estado.objects.get(pk=1),idusuario_creac=profile.numero)
        frmprovincia = ProvinciaForm(request.POST, instance=provincia) # A form bound to the POST data
        print request.POST  
        if frmprovincia.is_valid():
            frmprovincia.save()
            return redirect('/home/') # Crear un parametro en home para mostrar los mensajes de exito.
    else:        
        frmprovincia = ProvinciaForm()
    print frmprovincia.non_field_errors
    return render_to_response('ubigeo/provincia.html', {'frmprovincia': frmprovincia,'opcion':'add','usuario':request.session['nombres'],'fecha':request.session['login_date']}, context_instance=RequestContext(request),)

@login_required(login_url='/')
def provinciaedit(request, codigo):
    if request.method == 'POST':
        profile = Usuario.objects.get(user = request.user)
        provincia = Provincia.objects.get(numpro=int(codigo))
        provincia.idusuario_mod=profile.numero
        frmprovincia = ProvinciaForm(request.POST, instance=provincia) # A form bound to the POST data	
        if frmprovincia.is_valid():
            frmprovincia.save()
            return redirect('/home/') # Crear un parametro en home para mostrar los mensajes de exito.
    else:
        provincia = get_object_or_404(Provincia, numpro=int(codigo))
        frmprovincia = ProvinciaForm(instance=provincia)
    return render_to_response('ubigeo/provincia.html', {'frmprovincia': frmprovincia,'opcion':'edit','codigo':codigo,'usuario':request.session['nombres'],'fecha':request.session['login_date']}, context_instance=RequestContext(request),)

@login_required(login_url='/')
def provinciaquery(request):
    col = "-provincia"
    if "2-sort" in request.GET:
        col = request.GET['2-sort']
    provincias = Provincia.objects.all()
    config = RequestConfig(request)
    if request.method == "POST":
        consultaprovinciaform = ConsultaProvinciaForm(request.POST)        
        if consultaprovinciaform.is_valid():
            provincias = provincias.filter(provincia__icontains=request.POST['provincia'], region__region__icontains=request.POST['region']).order_by(col)
    else:
        consultaprovinciaform = ConsultaProvinciaForm()
    tblprovincias = ProvinciaTable(provincias.order_by(col))
    config.configure(tblprovincias)
    tblprovincias.paginate(page=request.GET.get('page', 1), per_page=6)
    return render_to_response('ubigeo/provincia_consulta.html', {'consultaprovinciaform':consultaprovinciaform,'tabla':tblprovincias,'usuario':request.session['nombres'],'fecha':request.session['login_date']}, context_instance=RequestContext(request),)

@login_required(login_url='/')
def jsonprovincia(request):
    provincias = Provincia.objects.filter(region = Region.objects.get(numreg = request.GET['r'])).order_by('provincia')
    return HttpResponse(serializers.serialize("json", provincias, ensure_ascii=False),mimetype='application/json')
