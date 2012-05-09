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
from django.http import HttpResponse, Http404
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
            obj=MaterialGrafico.objects.extra(where=[u"SUBSTRING_INDEX(arcmg1, '.', 1) ='materialgrafico/"+filename+"'",])[:1]
            if len(obj)>0:
                dobj = obj.values('arcmg1','arcmg2','arcmg3','arcmg4','arcmg5','arcmg6','arcmg7','arcmg8')
                for a in range(1,9):
                    fss.delete(dobj[0]['arcmg'+str(a)])
                obj = obj.get()
            else:    
                num = MaterialGrafico.objects.values("nummg").order_by("-nummg",)[:1]
                num = 1 if len(num)==0 else int(num[0]["nummg"])+1 
                obj = MaterialGrafico(nummg=num,organismo=profile.organismo,dependencia=profile.dependencia,idusuario_creac=profile.numero,)
            for archivo in request.FILES:   
                filename1 = request.FILES[archivo].name
                ext = filename1[filename1.rfind('.')+1:]
                filename= "MG%s%s_0%s.%s" % (ini.iniciales,datetime.today().strftime("%d%m%Y"),archivo[-1:],ext.upper())                
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
    filtro.append(u"materialgrafico.organismo_id=organismo.codigo")
    try:
        query = MaterialGrafico.objects.extra(tables=['usuario','organismo'],where=filtro,select={'organismo':'organismo.nombre','usuario':'usuario.usuario','dependencia':"case materialgrafico.organismo_id when 1 then (select ministerio from ministerio where nummin=materialgrafico.dependencia) when 2 then (select odp from odp where numodp=materialgrafico.dependencia) when 3 then (select gobernacion from gobernacion where numgob=materialgrafico.dependencia) end",'tipo1':"SUBSTRING_INDEX(arcmg1, '.', -1)",'tipo2':"SUBSTRING_INDEX(arcmg2, '.', -1)",'tipo3':"SUBSTRING_INDEX(arcmg3, '.', -1)",'tipo4':"SUBSTRING_INDEX(arcmg4, '.', -1)",'tipo5':"SUBSTRING_INDEX(arcmg5, '.', -1)",'tipo6':"SUBSTRING_INDEX(arcmg6, '.', -1)",'tipo7':"SUBSTRING_INDEX(arcmg7, '.', -1)",'tipo8':"SUBSTRING_INDEX(arcmg8, '.', -1)"}).order_by(col).values('organismo','dependencia','fec_creac','usuario','dependencia','urlmg1','urlmg2','urlmg3','urlmg4','urlmg5','urlmg6','urlmg7','urlmg8','tipo1','tipo2','tipo3','tipo4','tipo5','tipo6','tipo7','tipo8')
        data = list()
        dmg = dict()     
        for mg in query:
            for a in range(1,9):
                dmg = {'organismo':mg['organismo'],'dependencia':mg['dependencia'],'fec_creac':mg['fec_creac'],'usuario':mg['usuario'],'Descargar':mg['urlmg'+str(a)],'Tipo':mg['tipo'+str(a)]}
                data.append(dmg)          
        tabla = MGTable(data)
        config.configure(tabla)
        tabla.paginate(page=request.GET.get('page', 1), per_page=6)
        return render_to_response('extras/mg_consulta.html', {'formulario':formulario,'tabla':tabla,'usuario':request.session['nombres'],'fecha':request.session['login_date'],'dependencia':dependencia,'dep':request.session['dependencia']}, context_instance=RequestContext(request),)
    except:
        raise Http404

@login_required()
def mgprint(request):
    col = "-organismo"
    if "2-sort" in request.GET:
        col = request.GET['2-sort']
    filtro = list()
    if 'organismo' in request.GET:
        if request.GET['organismo']:
            filtro.append(u"materialgrafico.organismo_id =%s"%request.GET['organismo'])
        if 'dependencia' in request.GET:
            if request.GET['dependencia']:
                filtro.append(u"materialgrafico.dependencia =%s"%request.GET['dependencia'])
    filtro.append(u"idusuario_creac=usuario.numero")
    filtro.append(u"materialgrafico.organismo_id=organismo.codigo")
    query = MaterialGrafico.objects.extra(tables=['usuario','organismo'],where=filtro,select={'organismo':'organismo.nombre','usuario':'usuario.usuario','dependencia':"case materialgrafico.organismo_id when 1 then (select ministerio from ministerio where nummin=materialgrafico.dependencia) when 2 then (select odp from odp where numodp=materialgrafico.dependencia) when 3 then (select gobernacion from gobernacion where numgob=materialgrafico.dependencia) end",'tipo1':"SUBSTRING_INDEX(arcmg1, '.', -1)",'tipo2':"SUBSTRING_INDEX(arcmg2, '.', -1)",'tipo3':"SUBSTRING_INDEX(arcmg3, '.', -1)",'tipo4':"SUBSTRING_INDEX(arcmg4, '.', -1)",'tipo5':"SUBSTRING_INDEX(arcmg5, '.', -1)",'tipo6':"SUBSTRING_INDEX(arcmg6, '.', -1)",'tipo7':"SUBSTRING_INDEX(arcmg7, '.', -1)",'tipo8':"SUBSTRING_INDEX(arcmg8, '.', -1)"}).order_by(col).values('organismo','dependencia','fec_creac','usuario','dependencia','tipo1','tipo2','tipo3','tipo4','tipo5','tipo6','tipo7','tipo8')
    data = list()
    dmg = dict()     
    for mg in query:
        for a in range(1,9):
            dmg = {'organismo':mg['organismo'],'dependencia':mg['dependencia'],'fecha':mg['fec_creac'],'usuario':mg['usuario'],'tipo':mg['tipo'+str(a)]}
            data.append(dmg)
    filename= "mg_%s.csv" % datetime.today().strftime("%Y%m%d")
    return imprimirToExcel('extras/reportemg.html', {'data': data,'fecha':datetime.today().date(),'hora':datetime.today().time(),'usuario':request.session['nombres']},filename)
