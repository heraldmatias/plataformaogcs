# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, redirect
from forms import RegionForm, ProvinciaForm, ConsultaRegionForm, RegionTable, ConsultaProvinciaForm, ProvinciaTable
from django.template import RequestContext
from usuario.models import Usuario, Estado
from models import Region, Provincia
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.shortcuts import get_object_or_404
import django_tables2 as tables
from django_tables2.config import RequestConfig
from datetime import datetime
from scripts.scripts import imprimirToExcel, imprimirToPDF#, render_to_pdf_response
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string

@login_required()
def regionadd(request):
    mensaje=""
    if request.method == 'POST':
        profile = Usuario.objects.get(user = request.user)
        num = Region.objects.values("numreg").order_by("-numreg",)[:1]
        num = 1 if len(num)==0 else int(num[0]["numreg"])+1
        region = Region(numreg=num,estado=Estado.objects.get(pk=1),idusuario_creac=profile.numero,)
        frmregion = RegionForm(request.POST, instance=region) # A form bound to the POST data
        if frmregion.is_valid():
            for campo in frmregion.fields:
                frmregion.fields[campo]=request.POST[campo].upper()
            frmregion.save()
            frmregion = RegionForm() # Crear un parametro en home para mostrar los mensajes de exito.
            mensaje="Registro grabado satisfactoriamente."
    else:        
        frmregion = RegionForm()
    return render_to_response('ubigeo/region.html', {'frmregion': frmregion,'opcion':'add','mensaje':mensaje,}, context_instance=RequestContext(request),)

@login_required()
def regionedit(request, codigo):
    if request.method == 'POST':
        profile = Usuario.objects.get(user = request.user)
        region = Region.objects.get(numreg=int(codigo))
        region.idusuario_mod=profile.numero
        frmregion = RegionForm(request.POST, instance=region) # A form bound to the POST data	
        if frmregion.is_valid():
            frmregion.save()
            return redirect(reverse('ogcs-mantenimiento-region-consulta')+'?m=edit')
    else:
        region = get_object_or_404(Region, numreg=int(codigo))
        frmregion = RegionForm(instance=region)
    return render_to_response('ubigeo/region.html', {'frmregion': frmregion,'opcion':'edit','codigo':codigo}, context_instance=RequestContext(request),)

@login_required()
def regionprint(request):
    if "region" in request.GET:        
        qregiones = Region.objects.all().filter(region__icontains=request.GET['region']).order_by("region")
        html = render_to_string('ubigeo/reporter.html',{'data': qregiones,'pagesize':'A4','usuario':request.user.get_profile()},context_instance=RequestContext(request))
        filename= "region_%s.pdf" % datetime.today().strftime("%Y%m%d")        
        return imprimirToPDF(html,filename)

@login_required()
def regionquery(request):
    col = "-region"
    regiones = None
    if "2-sort" in request.GET:
        col = request.GET['2-sort']
    config = RequestConfig(request)
    consultaregionform = ConsultaRegionForm(request.GET)
    if "region" in request.GET:     
        regiones = Region.objects.filter(region__icontains=request.GET['region']).order_by(col)
    if regiones is None:
        regiones = Region.objects.all()
    tblregiones = RegionTable(regiones.order_by(col))
    config.configure(tblregiones)
    tblregiones.paginate(page=request.GET.get('page', 1), per_page=6)
    return render_to_response('ubigeo/region_consulta.html', {'consultaregionform':consultaregionform,'tblregiones':tblregiones,'mensaje':(request.GET['m'] if 'm' in request.GET else '')}, context_instance=RequestContext(request),)

@login_required()
def provinciaadd(request):
    profile = Usuario.objects.get(user = request.user)
    mensaje=""
    if request.method == 'POST':
        num = Provincia.objects.values("numpro").order_by("-numpro",)[:1]
        num = 1 if len(num)==0 else int(num[0]["numpro"])+1
        provincia = Provincia(numpro=num,estado=Estado.objects.get(pk=1),idusuario_creac=profile.numero)
        frmprovincia = ProvinciaForm(request.POST, instance=provincia) # A form bound to the POST data
        if frmprovincia.is_valid():
            frmprovincia.save()
            frmprovincia = ProvinciaForm()  
            mensaje="Registro grabado satisfactoriamente." # Crear un parametro en home para mostrar los mensajes de exito.
    else:        
        frmprovincia = ProvinciaForm()
    return render_to_response('ubigeo/provincia.html', {'frmprovincia': frmprovincia,'opcion':'add','mensaje':mensaje}, context_instance=RequestContext(request),)

@login_required()
def provinciaedit(request, codigo):
    if request.method == 'POST':
        profile = Usuario.objects.get(user = request.user)
        provincia = Provincia.objects.get(numpro=int(codigo))
        provincia.idusuario_mod=profile.numero
        frmprovincia = ProvinciaForm(request.POST, instance=provincia) # A form bound to the POST data	
        if frmprovincia.is_valid():
            frmprovincia.save()
            return redirect(reverse('ogcs-mantenimiento-provincia-consulta')+'?m=edit')
    else:
        provincia = get_object_or_404(Provincia, numpro=int(codigo))
        frmprovincia = ProvinciaForm(instance=provincia)
    return render_to_response('ubigeo/provincia.html', {'frmprovincia': frmprovincia,'opcion':'edit','codigo':codigo,}, context_instance=RequestContext(request),)

@login_required()
def provinciaquery(request):
    col = "-provincia"
    if "2-sort" in request.GET:
        col = request.GET['2-sort']
    config = RequestConfig(request)
    consultaprovinciaform = ConsultaProvinciaForm(request.GET)
    if 'region' in request.GET and 'provincia' in request.GET:
        if (request.GET['region'] and request.GET['provincia']) or request.GET['region']:
            provincias = Provincia.objects.filter(provincia__icontains=request.GET['provincia'], region=request.GET['region']).order_by(col)
        elif request.GET['provincia']:
            provincias = Provincia.objects.filter(provincia__icontains=request.GET['provincia'],).order_by(col)
        else:
            provincias = Provincia.objects.all().order_by(col)
    else:
       provincias = Provincia.objects.all().order_by(col)
    tblprovincias = ProvinciaTable(provincias.order_by(col))
    config.configure(tblprovincias)
    tblprovincias.paginate(page=request.GET.get('page', 1), per_page=6)
    return render_to_response('ubigeo/provincia_consulta.html', {'consultaprovinciaform':consultaprovinciaform,'tabla':tblprovincias,'mensaje':(request.GET['m'] if 'm' in request.GET else '')}, context_instance=RequestContext(request),)

@login_required()
def provinciaprint(request):
    col = 'provincia'
    if (request.GET['region'] and request.GET['provincia']) or request.GET['region']:
        provincias = Provincia.objects.filter(provincia__icontains=request.GET['provincia'], region=request.GET['region']).order_by(col)
    elif request.GET['provincia']:
        provincias = Provincia.objects.filter(provincia__icontains=request.GET['provincia'],).order_by(col)
    else:
        provincias = Provincia.objects.all().order_by(col)
    html = render_to_string('ubigeo/reportep.html',{'data': provincias,'pagesize':'A4','usuario':request.user.get_profile()},context_instance=RequestContext(request))
    filename= "provincia_%s.pdf" % datetime.today().strftime("%Y%m%d")        
    return imprimirToPDF(html,filename)

@login_required()
def jsonprovincia(request):
    if request.GET['r']:
        provincias = Provincia.objects.filter(region = Region.objects.get(numreg = request.GET['r'])).order_by('provincia')
    else:
        provincias = {}
    return HttpResponse(serializers.serialize("json", provincias, ensure_ascii=False),mimetype='application/json')
