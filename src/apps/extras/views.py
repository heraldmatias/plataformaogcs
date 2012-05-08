# -*- coding: utf-8 -*-
from forms import *
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext
from models import MaterialGrafico
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.shortcuts import get_object_or_404
import django_tables2 as tables
from django_tables2.config import RequestConfig
from datetime import datetime
from scripts.scripts import imprimirToExcel
from django.http import HttpResponse
from django.core.files.storage import  FileSystemStorage

@login_required()
def mgadd(request):
    mensaje=""
    if request.method == 'POST':               
        if 'arcmg1' in request.FILES and 'arcmg2' in request.FILES and 'arcmg3' in request.FILES and 'arcmg4' in request.FILES and 'arcmg5' in request.FILES and 'arcmg6' in request.FILES and 'arcmg7' in request.FILES and 'arcmg8' in request.FILES:
            profile = request.user.get_profile()
            ini=request.session['dependencia']            
            fss = FileSystemStorage()
            filename= "MG%s%s_01" % (ini.iniciales,datetime.today().strftime("%d%m%Y"))
            try:
                obj=MaterialGrafico.objects.extra(where=[u"SUBSTRING_INDEX(arcmg1, '.', 1) ='materialgrafico/"+filename+"'",])[:1].get()
            except:
                num = MaterialGrafico.objects.values("nummg").order_by("-nummg",)[:1]
                num = 1 if len(num)==0 else int(num[0]["nummg"])+1 
                obj = MaterialGrafico(nummg=num,organismo=profile.organismo,dependencia=profile.dependencia,idusuario_creac=profile.numero,)
            for archivo in request.FILES:   
                filename1 = request.FILES[archivo].name
                ext = filename1[filename1.rfind('.')+1:]
                filename= "MG%s%s_0%s.%s" % (ini.iniciales,datetime.today().strftime("%d%m%Y"),archivo[-1:],ext.upper())
                fss.delete('materialgrafico/'+filename)
                request.FILES[archivo].name = filename               
            formulario = MGForm(request.POST,request.FILES,instance=obj ) # A form bound to the POST data
            if formulario.is_valid():
                formulario.save()
                obj.urlmg1= obj.arcmg1.url
                obj.urlmg2= obj.arcmg2.url
                obj.urlmg3= obj.arcmg3.url
                obj.urlmg4= obj.arcmg4.url
                obj.urlmg5= obj.arcmg5.url
                obj.urlmg6= obj.arcmg6.url
                obj.urlmg7= obj.arcmg7.url
                obj.urlmg8= obj.arcmg8.url
                obj.save()
                mensaje="Registro grabado satisfactoriamente."
        formulario = MGForm() # Crear un parametro en home para mostrar los mensajes de exito.            
    else:        
        formulario = MGForm()
    return render_to_response('extras/mg.html', {'formulario': formulario,'usuario':request.session['nombres'],'fecha':request.session['login_date'],'mensaje':mensaje,'dep':request.session['dependencia']}, context_instance=RequestContext(request),)

@login_required()
def mgquery(request):
    col = "-organismo"
    query = None
    dependencia=''
    filtro = list()
    if "2-sort" in request.GET:
        col = request.GET['2-sort']
    config = RequestConfig(request)
    formulario = ConsultaMGForm(request.GET)
    if 'organismo' in request.GET:
        if request.GET['organismo']:
            filtro.append(u"materialgrafico.organismo_id =%s"%request.GET['organismo'])
        if 'dependencia' in request.GET:
            if request.GET['dependencia']:
                filtro.append(u"materialgrafico.dependencia =%s"%request.GET['dependencia'])
                dependencia=request.GET['dependencia']
    filtro.append(u"idusuario_creac=usuario.numero")
    query = MaterialGrafico.objects.extra(tables=['usuario',],where=filtro,select={'usuario':'usuario.usuario','dependencia':"case materialgrafico.organismo_id when 1 then (select ministerio from ministerio where nummin=materialgrafico.dependencia) when 2 then (select odp from odp where numodp=materialgrafico.dependencia) when 3 then (select gobernacion from gobernacion where numgob=materialgrafico.dependencia) end"}).order_by(col).values()
    
    tabla = MGTable(query)
    config.configure(tabla)
    tabla.paginate(page=request.GET.get('page', 1), per_page=6)
    return render_to_response('extras/mg_consulta.html', {'formulario':formulario,'tabla':tabla,'usuario':request.session['nombres'],'fecha':request.session['login_date'],'dependencia':dependencia,'dep':request.session['dependencia']}, context_instance=RequestContext(request),)

@login_required()
def mgprint(request):
    filtro = list()
    if 'organismo' in request.GET:
        if request.GET['organismo']:
            filtro.append(u"oac.organismo_id =%s"%request.GET['organismo'])
        if 'dependencia' in request.GET:
            if request.GET['dependencia']:
                filtro.append(u"oac.dependencia =%s"%request.GET['dependencia'])
    filtro.append(u"idusuario_creac=usuario.numero")
    query = Oac.objects.extra(tables=['usuario',],where=filtro,select={'usuario':'usuario.usuario','dependencia':"case oac.organismo_id when 1 then (select ministerio from ministerio where nummin=oac.dependencia) when 2 then (select odp from odp where numodp=oac.dependencia) when 3 then (select gobernacion from gobernacion where numgob=oac.dependencia) end"})
    filename= "oac_%s.csv" % datetime.today().strftime("%Y%m%d")
    return imprimirToExcel('comunicacion/reporteoac.html', {'data': query,'fecha':datetime.today().date(),'hora':datetime.today().time(),'usuario':request.session['nombres']},filename)
