# -*- coding: utf-8 -*-
from forms import *
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext
#from usuario.models import Usuario, Estado
#from dependencia.models import Ministerio, Odp, Gobernacion
from models import *
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.shortcuts import get_object_or_404
import django_tables2 as tables
from django_tables2.config import RequestConfig
from datetime import datetime
from scripts.scripts import imprimirToExcel
from django.http import HttpResponse
#from django.core.files import File
from django.core.files.storage import  FileSystemStorage

@login_required()
def oacadd(request):
    mensaje=""
    if request.method == 'POST':               
        if 'archivo' in request.FILES:
            profile = request.user.get_profile()
            ini=request.session['dependencia']      
            filename= "OAC%s%s.pdf" % (ini.iniciales,datetime.today().strftime("%d%m%Y"))
            try:
                obj=Oac.objects.get(archivo='oac/'+filename)
            except:
                num = Oac.objects.values("numoac").order_by("-numoac",)[:1]
                num = 1 if len(num)==0 else int(num[0]["numoac"])+1
                obj = Oac(numoac=num,organismo=profile.organismo,dependencia=profile.dependencia,idusuario_creac=profile.numero,)
            FileSystemStorage().delete('oac/'+filename)
            request.FILES['archivo'].name = filename
        formulario = OacForm(request.POST,request.FILES,instance=obj ) # A form bound to the POST data
        if formulario.is_valid():
            formulario.save()
            obj.urloac= obj.archivo.url
            obj.save()
            formulario = OacForm() # Crear un parametro en home para mostrar los mensajes de exito.
            mensaje="Registro grabado satisfactoriamente."
    else:        
        formulario = OacForm()
    return render_to_response('comunicacion/oac.html', {'formulario': formulario,'usuario':request.session['nombres'],'fecha':request.session['login_date'],'mensaje':mensaje,'dep':request.session['dependencia']}, context_instance=RequestContext(request),)

@login_required()
def oacquery(request):
    col = "-organismo"
    query = None
    dependencia=''
    filtro = list()
    if "2-sort" in request.GET:
        col = request.GET['2-sort']
    config = RequestConfig(request)
    formulario = ConsultaOacForm(request.GET)
    if 'organismo' in request.GET:
        if request.GET['organismo']:
            filtro.append(u"oac.organismo_id =%s"%request.GET['organismo'])
        if 'dependencia' in request.GET:
            if request.GET['dependencia']:
                filtro.append(u"oac.dependencia =%s"%request.GET['dependencia'])
                dependencia=request.GET['dependencia']
    filtro.append(u"idusuario_creac=usuario.numero")
    query = Oac.objects.extra(tables=['usuario',],where=filtro,select={'usuario':'usuario.usuario','dependencia':"case oac.organismo_id when 1 then (select ministerio from ministerio where nummin=oac.dependencia) when 2 then (select odp from odp where numodp=oac.dependencia) when 3 then (select gobernacion from gobernacion where numgob=oac.dependencia) end"})
    tabla = OacTable(query.order_by(col))
    config.configure(tabla)
    tabla.paginate(page=request.GET.get('page', 1), per_page=6)
    return render_to_response('comunicacion/oac_consulta.html', {'formulario':formulario,'tabla':tabla,'usuario':request.session['nombres'],'fecha':request.session['login_date'],'dependencia':dependencia,'dep':request.session['dependencia']}, context_instance=RequestContext(request),)

@login_required()
def oacprint(request):
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

@login_required()
def pgcsadd(request):
    mensaje=""
    if request.method == 'POST':               
        if 'archivo' in request.FILES:
            profile = request.user.get_profile() 
            ini=request.session['dependencia']
            filename= "PGCS%s%s.pdf" % (ini.iniciales,datetime.today().strftime("%d%m%Y"))
            try:
                obj=Pgcs.objects.get(archivo='pgcs/'+filename)
            except:
                num = Pgcs.objects.values("numpgcs").order_by("-numpgcs",)[:1]
                num = 1 if len(num)==0 else int(num[0]["numpgcs"])+1
                obj = Pgcs(numpgcs=num,organismo=profile.organismo,dependencia=profile.dependencia,idusuario_creac=profile.numero,tipopgcs=TipoOgcs.objects.get(codigo=1))
            FileSystemStorage().delete('pgcs/'+filename)
            request.FILES['archivo'].name = filename
        formulario = PgcsForm(request.POST,request.FILES,instance=obj ) # A form bound to the POST data
        if formulario.is_valid():
            formulario.save()
            obj.urlpgcs= obj.archivo.url
            obj.save()
            formulario = PgcsForm() # Crear un parametro en home para mostrar los mensajes de exito.
            mensaje="Registro grabado satisfactoriamente."
    else:        
        formulario = PgcsForm()
    return render_to_response('comunicacion/pgcs.html', {'formulario': formulario,'usuario':request.session['nombres'],'fecha':request.session['login_date'],'mensaje':mensaje,'dep':request.session['dependencia']}, context_instance=RequestContext(request),)

@login_required()
def pgcsquery(request):
    col = "-organismo"
    query = None
    dependencia=''
    filtro = list()
    if "2-sort" in request.GET:
        col = request.GET['2-sort']
    config = RequestConfig(request)
    formulario = ConsultaPgcsForm(request.GET)
    if 'organismo' in request.GET:
        if request.GET['organismo']:
            filtro.append(u"pgcs.organismo_id =%s"%request.GET['organismo'])
        if 'dependencia' in request.GET:
            if request.GET['dependencia']:
                filtro.append(u"pgcs.dependencia =%s"%request.GET['dependencia'])
                dependencia=request.GET['dependencia']
    filtro.append(u"idusuario_creac=usuario.numero")
    filtro.append(u"tipopgcs_id=1")
    query = Pgcs.objects.extra(tables=['usuario',],where=filtro,select={'usuario':'usuario.usuario','dependencia':"case pgcs.organismo_id when 1 then (select ministerio from ministerio where nummin=pgcs.dependencia) when 2 then (select odp from odp where numodp=pgcs.dependencia) when 3 then (select gobernacion from gobernacion where numgob=pgcs.dependencia) end"})
    tabla = PgcsTable(query.order_by(col))
    config.configure(tabla)
    tabla.paginate(page=request.GET.get('page', 1), per_page=6)
    return render_to_response('comunicacion/pgcs_consulta.html', {'formulario':formulario,'tabla':tabla,'usuario':request.session['nombres'],'fecha':request.session['login_date'],'dependencia':dependencia,'dep':request.session['dependencia']}, context_instance=RequestContext(request),)

@login_required()
def pgcsprint(request,tipo):
    filtro = list()
    if 'organismo' in request.GET:
        if request.GET['organismo']:
            filtro.append(u"oac.organismo_id =%s"%request.GET['organismo'])
        if 'dependencia' in request.GET:
            if request.GET['dependencia']:
                filtro.append(u"oac.dependencia =%s"%request.GET['dependencia'])
    filtro.append(u"idusuario_creac=usuario.numero")    
    filtro.append(u"tipopgcs_id="+str(tipo))
    query = Pgcs.objects.extra(tables=['usuario',],where=filtro,select={'usuario':'usuario.usuario','dependencia':"case pgcs.organismo_id when 1 then (select ministerio from ministerio where nummin=pgcs.dependencia) when 2 then (select odp from odp where numodp=pgcs.dependencia) when 3 then (select gobernacion from gobernacion where numgob=pgcs.dependencia) end"})
    filename= ("pgcs_%s.csv" if tipo=="1" else "pgcsaporte_%s.csv") % datetime.today().strftime("%Y%m%d")
    return imprimirToExcel('comunicacion/reportepgcs.html' if tipo=="1" else 'comunicacion/reporte_pgcs_aporte.html', {'data': query,'fecha':datetime.today().date(),'hora':datetime.today().time(),'usuario':request.session['nombres']},filename)

@login_required()
def pgcs_apor_add(request):
    mensaje=""
    if request.method == 'POST':               
        if 'archivo' in request.FILES:
            profile = request.user.get_profile() 
            ini=request.session['dependencia']
            archivo=request.FILES['archivo'].name
            filename= "PGCSAPORTE%s%s%s" % (ini.iniciales,datetime.today().strftime("%d%m%Y"),archivo[archivo.rfind('.'):])
            try:
                obj=Pgcs.objects.get(archivo='pgcs/'+filename)
            except:
                num = Pgcs.objects.values("numpgcs").order_by("-numpgcs",)[:1]
                num = 1 if len(num)==0 else int(num[0]["numpgcs"])+1
                obj = Pgcs(numpgcs=num,organismo=profile.organismo,dependencia=profile.dependencia,idusuario_creac=profile.numero,tipopgcs=TipoOgcs.objects.get(codigo=2))
            FileSystemStorage().delete('pgcs/'+filename)
            request.FILES['archivo'].name = filename
        formulario = PgcsForm(request.POST,request.FILES,instance=obj ) # A form bound to the POST data
        if formulario.is_valid():
            formulario.save()
            obj.urlpgcs= obj.archivo.url
            obj.save()
            formulario = PgcsForm() # Crear un parametro en home para mostrar los mensajes de exito.
            mensaje="Registro grabado satisfactoriamente."
    else:        
        formulario = PgcsForm()
    return render_to_response('comunicacion/pgcs.html', {'formulario': formulario,'usuario':request.session['nombres'],'fecha':request.session['login_date'],'mensaje':mensaje,'aporte':'aporte','dep':request.session['dependencia']}, context_instance=RequestContext(request),)

@login_required()
def pgcs_apor_query(request):
    col = "-organismo"
    query = None
    dependencia=''
    filtro = list()
    if "2-sort" in request.GET:
        col = request.GET['2-sort']
    config = RequestConfig(request)
    formulario = ConsultaPgcsForm(request.GET)
    if 'organismo' in request.GET:
        if request.GET['organismo']:
            filtro.append(u"pgcs.organismo_id =%s"%request.GET['organismo'])
        if 'dependencia' in request.GET:
            if request.GET['dependencia']:
                filtro.append(u"pgcs.dependencia =%s"%request.GET['dependencia'])
                dependencia=request.GET['dependencia']
    filtro.append(u"idusuario_creac=usuario.numero")
    filtro.append(u"tipopgcs_id=2")
    query = Pgcs.objects.extra(tables=['usuario',],where=filtro,select={'usuario':'usuario.usuario','dependencia':"case pgcs.organismo_id when 1 then (select ministerio from ministerio where nummin=pgcs.dependencia) when 2 then (select odp from odp where numodp=pgcs.dependencia) when 3 then (select gobernacion from gobernacion where numgob=pgcs.dependencia) end"})
    tabla = PgcsTable(query.order_by(col))
    config.configure(tabla)
    tabla.paginate(page=request.GET.get('page', 1), per_page=6)
    return render_to_response('comunicacion/pgcs_consulta.html', {'formulario':formulario,'tabla':tabla,'usuario':request.session['nombres'],'fecha':request.session['login_date'],'dependencia':dependencia,'aporte':'aporte','dep':request.session['dependencia']}, context_instance=RequestContext(request),)

######################## MCCA INICIO ###############################################
####################################################################################


def mccaadd(request):
    mensaje=""
    if request.method == 'POST':
		#sectores_estado
		corg = request.POST.getlist('corg')
		cdep = request.POST.getlist('cdep')
		#secores_privado
		cpri = request.POST.getlist('cpri')
		#indicadores
		cind = request.POST.getlist('cind')
		#mensajes
		cmen = request.POST.getlist('cmen')
		#canales
		ctipo = request.POST.getlist('ctipo')
		ccan = request.POST.getlist('ccan')
		#acciones
		cacc = request.POST.getlist('cacc')
		caccfini = request.POST.getlist('caccfini')
		caccffin = request.POST.getlist('caccffin')
		#observaciones
		cobs = request.POST.getlist('cobs')
		#Proceso de escritura en la BD
		#profile = request.user.get_profile() 
		#ini=request.session['dependencia']
		num = Mcca.objects.values("nummcca").order_by("-nummcca",)[:1]
		num = 1 if len(num)==0 else int(num[0]["nummcca"])+1
		fecini = request.POST["fechaini"]
		fecfin = request.POST["fechafin"]
		fecini = datetime.strptime(fecini, "%d/%m/%Y").strftime("%Y-%m-%d")
		fecfin = datetime.strptime(fecfin, "%d/%m/%Y").strftime("%Y-%m-%d")
		obj = Mcca(nummcca=num,nombremmca=request.POST["nombremmca"],fechaini=fecini,fechafin=fecfin,organismo=profile.organismo,dependencia=profile.dependencia,idusuario_creac=profile.numero,publico='ninguno')
		#formmcca = MccaForm(request.POST,instance=obj)
		#if formmcca.is_valid():
		obj.save()
		#sectores_Estado_save
		for c in range(len(corg)): 
			MccaEstado(nummcca=obj,item=c,organismo=Organismo.objects.get(codigo=corg[c]),dependencia=cdep[c]).save()
		#sectores_privado_save
		for c in range(len(cpri)):
			MccaPrivado(nummcca=obj,item=c,privado=cpri[c],auditoria=1).save()
		#indicadores_save
		for c in range(len(cind)):
			MccaIndicador(nummcca=obj,item=c,indicador=cind[c],auditoria=1).save()
		#mensajes_save
		for c in range(len(cmen)): 
			MccaMensaje(nummcca=obj,item=c,mensaje=cmen[c],auditoria=1).save()
		#canales_save
		for c in range(len(ccan)):
			MccaCanal(nummcca=obj,item=c,tipommca=MccaTipoComunicacion.objects.get(codigo=ctipo[c]),canal=ccan[c],auditoria=1).save()
		#acciones_save
		for c in range(len(cacc)):
			MccaAccion(nummcca = obj,item =c, fechainia=caccfini[c],fechafina=caccffin[c], acciones=cacc[c], auditoria=1).save()
		#observaciones_save
		for c in range(len(cobs)):
			MccaObservacion(nummcca=obj,item=c,observacion=cobs[c],auditoria=1).save()
		formmcca = MccaForm() # Crear un parametro en home para mostrar los mensajes de exito.
		mensaje="Registro grabado satisfactoriamente."
    else:        
        formmcca = MccaForm()
    tabla = MccaForm_EstadoTable(list())
    tabla1 = MccaForm_PrivadoTable(list())
    tabla2 = MccaForm_IndicadorTable(list())
    tabla3 = MccaForm_MensajeTable(list())
    tabla4 = MccaForm_CanalTable(list())
    tabla5 = MccaForm_AccionTable(list())       
    tabla6 = MccaForm_ObservacionTable(list())        
    formmcca_estado = MccaForm_Estado()
    formmcca_privado = MccaForm_Privado()
    formmcca_indicador = MccaForm_Indicador()
    formmcca_mensaje = MccaForm_Mensaje()
    formmcca_canal = MccaForm_Canal()
    formmcca_accion = MccaForm_Accion()
    formmcca_observacion = MccaForm_Observacion()
    return render_to_response('comunicacion/mcca.html', {'form': formmcca,'form_estado': formmcca_estado,'form_privado': formmcca_privado,'form_indicador': formmcca_indicador,'form_mensaje': formmcca_mensaje,'form_canal': formmcca_canal,'form_accion': formmcca_accion,'form_observacion': formmcca_observacion,'tabla':tabla,'tabla1':tabla1,'tabla2':tabla2,'tabla3':tabla3,'tabla4':tabla4,'tabla5':tabla5,'tabla6':tabla6,'mensaje':mensaje}, context_instance=RequestContext(request),)



def mcca_query(request):
    col = "-organismo"
    query = list()
    dependencia=''
    nombremmca=''
    fechaini=''
    fechafin=''
    filtro = list()
    if "2-sort" in request.GET:
        col = request.GET['2-sort']
    config = RequestConfig(request)
    form_estado = MccaForm_Estado(request.GET)
    form = MccaForm(request.GET)
    #if 'organismo' in request.GET:
    #    if request.GET['organismo']:
    #        filtro.append(u"pgcs.organismo_id =%s"%request.GET['organismo'])
    #    if 'dependencia' in request.GET:
    #        if request.GET['dependencia']:
    #            filtro.append(u"pgcs.dependencia =%s"%request.GET['dependencia'])
    #            dependencia=request.GET['dependencia']
    #filtro.append(u"idusuario_creac=usuario.numero")
    #filtro.append(u"tipopgcs_id=1")
    #query = Pgcs.objects.extra(tables=['usuario',],where=filtro,select={'usuario':'usuario.usuario','dependencia':"case pgcs.organismo_id when 1 then (select ministerio from ministerio where nummin=pgcs.dependencia) when 2 then (select odp from odp where numodp=pgcs.dependencia) when 3 then (select gobernacion from gobernacion where numgob=pgcs.dependencia) end"})
    #tabla = PgcsTable(query.order_by(col))
    tabla = MccaTable(query)
    config.configure(tabla)
    tabla.paginate(page=request.GET.get('page', 1), per_page=6)
    return render_to_response('comunicacion/mcca_consulta.html', {'form':form,'form_estado':form_estado,'tabla':tabla}, context_instance=RequestContext(request),)


######################## MCCA FINAL ################################################
####################################################################################


######################## MCC INICIO ###############################################
####################################################################################


def mccadd(request):
    mensaje=""
    query1 = list()
    query2 = list()
    query3 = list()
    if request.method == 'POST':
        if 'archivo' in request.FILES:
            profile = request.user.get_profile()
            ini=request.session['dependencia']
            filename= "PGCS%s%s.pdf" % (ini.iniciales,datetime.today().strftime("%d%m%Y"))
            try:
                obj=Pgcs.objects.get(archivo='pgcs/'+filename)
            except:
                num = Pgcs.objects.values("numpgcs").order_by("-numpgcs",)[:1]
                num = 1 if len(num)==0 else int(num[0]["numpgcs"])+1
                obj = Pgcs(numpgcs=num,organismo=profile.organismo,dependencia=profile.dependencia,idusuario_creac=profile.numero,tipopgcs=TipoOgcs.objects.get(codigo=1))
            FileSystemStorage().delete('pgcs/'+filename)
            request.FILES['archivo'].name = filename
        formulario = PgcsForm(request.POST,request.FILES,instance=obj ) # A form bound to the POST data
        if formulario.is_valid():
            formulario.save()
            obj.urlpgcs= obj.archivo.url
            obj.save()
            formmcca = MccaForm() # Crear un parametro en home para mostrar los mensajes de exito.
            mensaje="Registro grabado satisfactoriamente."
    else:
       
        #query1 = [
        #                {'item':'1','numtipovarios': '2','actor':'moises','institucion':'zzzz'},
        #]
        #
        #query2 = [
        #                {'item':'1','numtipovarios': '2','lider':'moises','institucion':'xxxx'},
        #]
        #
        #query3 = [
        #                {'item':'1','observacion': 'Django Reinhardt'},
        #]        

        tabla1 = MccForm_ActorTable(list())
        config.configure(tabla1)

        tabla2 = MccForm_LiderTable(list())
        config.configure(tabla2)

        tabla3 = MccForm_ObservacionTable(list())
        config.configure(tabla3)

        formmcc = MccForm()
        formmcc_lider = MccForm_Lider()
        formmcc_actor = MccForm_Actor()
        formmcc_observacion = MccForm_Observacion()

    return render_to_response('comunicacion/mcc.html', {'form': formmcc,'form_actor': formmcc_actor,'form_lider': formmcc_lider,'form_observacion':formmcc_observacion,'tabla1':tabla1,'tabla2':tabla2,'tabla3':tabla3,'mensaje':mensaje}, context_instance=RequestContext(request),)


def mccadd_actor(request):
    query = list()
    if(request.GET['tipo']=="add"):
        if("actores" in request.session):
            query =request.session['actores']
            num=len(query)+1
        else:
            num = 1
        query.extend([{'item':num,'numtipovarios': request.GET['varios'],'actor':request.GET['actor'],'institucion':request.GET['inst']}])
        request.session['actores'] = query
    else:
        if("actores" in request.session):
            query =request.session['actores']
        num=int(request.GET['actor'])-1
        query.pop(num);
        request.session['actores'] = query

    return query

def mccadd_lider(request):
    query = list()
    if(request.GET['tipo']=="add"):
        if("lideres" in request.session):
            query =request.session['lideres']
            num=len(query)+1
        else:
            num = 1
        query.extend([{'item':num,'numtipovarios': request.GET['varios'],'lider':request.GET['lider'],'institucion':request.GET['inst']}])
        request.session['lideres'] = query
    else:
        if("lideres" in request.session):
            query =request.session['lideres']
        num=int(request.GET['lider'])-1
        query.pop(num);
        request.session['lideres'] = query

    return query
	
def mccadd_observacion(request):
    query = list()
    if(request.GET['tipo']=="add"):
        if("observaciones_mcc" in request.session):
            query =request.session['observaciones_mcc']
            num=len(query)+1
        else:
            num = 1
        query.extend([{'item':num,'observacion': request.GET['obs']}])
        request.session['observaciones_mcc'] = query
    else:
        if("observaciones_mcc" in request.session):
            query =request.session['observaciones_mcc']
        num=int(request.GET['obs'])-1
        query.pop(num);
        request.session['observaciones_mcc'] = query


    return query



def mcc_query(request):
    col = "-organismo"
    query = list()
    dependencia=''
    nombremmca=''
    fechaini=''
    fechafin=''
    filtro = list()
    if "2-sort" in request.GET:
        col = request.GET['2-sort']
    config = RequestConfig(request)
    #form_estado = MccaForm_Estado(request.GET)
    form = MccForm(request.GET)
    #if 'organismo' in request.GET:
    #    if request.GET['organismo']:
    #        filtro.append(u"pgcs.organismo_id =%s"%request.GET['organismo'])
    #    if 'dependencia' in request.GET:
    #        if request.GET['dependencia']:
    #            filtro.append(u"pgcs.dependencia =%s"%request.GET['dependencia'])
    #            dependencia=request.GET['dependencia']
    #filtro.append(u"idusuario_creac=usuario.numero")
    #filtro.append(u"tipopgcs_id=1")
    #query = Pgcs.objects.extra(tables=['usuario',],where=filtro,select={'usuario':'usuario.usuario','dependencia':"case pgcs.organismo_id when 1 then (select ministerio from ministerio where nummin=pgcs.dependencia) when 2 then (select odp from odp where numodp=pgcs.dependencia) when 3 then (select gobernacion from gobernacion where numgob=pgcs.dependencia) end"})
    #tabla = PgcsTable(query.order_by(col))
    tabla = MccTable(query)
    config.configure(tabla)
    tabla.paginate(page=request.GET.get('page', 1), per_page=6)
    return render_to_response('comunicacion/mcc_consulta.html', {'form':form, 'tabla':tabla }, context_instance=RequestContext(request),)

	

######################## MCC FINAL ################################################
####################################################################################
