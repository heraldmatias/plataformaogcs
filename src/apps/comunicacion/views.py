# -*- coding: utf-8 -*-
from forms import *
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext
#from usuario.models import Usuario, Estado
#from dependencia.models import Ministerio, Odp, Gobernacion
from models import Oac, Pgcs, TipoOgcs
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
    query = list()
    query1 = list()
    query2 = list()
    query3 = list()
    query4 = list()
    query5 = list()
    query6 = list()
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
        #query = [
        #                {'item':'1','organismo': 'Django Reinhardt', 'dependencia': 'jazz'},
        #]
        #query1 = [
        #                {'item':'1','privado': 'Django Reinhardt'},
        #]
        #query2 = [
        #                {'item':'1','indicador': 'Django Reinhardt'},
        #]
        #query3 = [
        #                {'item':'1','mensaje': 'Django Reinhardt'},
        #]
        #
        #query4 = [
        #                {'item':'1','canal': 'Django Reinhardt','tipommca_id':'1'},
        #]
        #
        #query5 = [
        #                {'item':'1','accion': 'Django Reinhardt','fechaini':'09-05-2012','fechafin':'15-05-2012'},
        #]
        #
        #query6 = [
        #                {'item':'1','observacion': 'Django Reinhardt'},
        #]
        config = RequestConfig(request)
       
        if 'id_org' in request.GET:
            query =mccaadd_estado(request)
            
        if("estados" in request.session):
            query =request.session['estados']
        #del request.session["estados"]

        if 'privado' in request.GET:
            query1 =mccaadd_privado(request)
            
        if("privados" in request.session):
            query1 =request.session['privados']
        
        if 'indicador' in request.GET:
            query2 =mccaadd_indicador(request)

        if("indicadores" in request.session):
            query2 =request.session['indicadores']

        if 'mensaje' in request.GET:
            query3 =mccaadd_mensaje(request)

        if("mensajes" in request.session):
            query3 =request.session['mensajes']

        if 'canal' in request.GET:
            query4 =mccaadd_canal(request)

        if("canales" in request.session):
            query4 =request.session['canales']

        if 'accion' in request.GET:
            query5 =mccaadd_accion(request)

        if("acciones" in request.session):
            query5 =request.session['acciones']

        if 'obs' in request.GET:
            query6 =mccaadd_observacion(request)

        if("observaciones" in request.session):
            query6 =request.session['observaciones']

        
        tabla = MccaForm_EstadoTable(query)
        config.configure(tabla)

        tabla1 = MccaForm_PrivadoTable(query1)
        config.configure(tabla1)

        tabla2 = MccaForm_IndicadorTable(query2)
        config.configure(tabla2)

        tabla3 = MccaForm_MensajeTable(query3)
        config.configure(tabla3)

        tabla4 = MccaForm_CanalTable(query4)
        config.configure(tabla4)

        tabla5 = MccaForm_AccionTable(query5)
        config.configure(tabla5)
        
        tabla6 = MccaForm_ObservacionTable(query6)
        config.configure(tabla6)
        
        formmcca = MccaForm()
        formmcca_estado = MccaForm_Estado()
        formmcca_privado = MccaForm_Privado()
        formmcca_indicador = MccaForm_Indicador()
        formmcca_mensaje = MccaForm_Mensaje()
        formmcca_canal = MccaForm_Canal()
        formmcca_accion = MccaForm_Accion()
        formmcca_observacion = MccaForm_Observacion()

    return render_to_response('comunicacion/mcca.html', {'form': formmcca,'form_estado': formmcca_estado,'form_privado': formmcca_privado,'form_indicador': formmcca_indicador,'form_mensaje': formmcca_mensaje,'form_canal': formmcca_canal,'form_accion': formmcca_accion,'form_observacion': formmcca_observacion,'tabla':tabla,'tabla1':tabla1,'tabla2':tabla2,'tabla3':tabla3,'tabla4':tabla4,'tabla5':tabla5,'tabla6':tabla6,'mensaje':mensaje}, context_instance=RequestContext(request),)


def mccaadd_estado(request):
    query = list()
    if(request.GET['tipo']=="add"):
        if("estados" in request.session):
            query =request.session['estados']
            num=len(query)+1
        else:
            num = 1
        query.extend([{'item':num,'organismo': request.GET['id_org'], 'dependencia': request.GET['id_dep']}])
        request.session['estados'] = query
    else:
        if("estados" in request.session):
            query =request.session['estados']
        num=int(request.GET['id_org'])-1
        query.pop(num);
        request.session['estados'] = query

        
    return query


def mccaadd_privado(request):
    query = list()
    if(request.GET['tipo']=="add"):
        if("privados" in request.session):
            query =request.session['privados']
            num=len(query)+1
        else:
            num = 1
        query.extend([{'item':num,'privado': request.GET['privado']}])
        request.session['privados'] = query
    else:
        if("privados" in request.session):
            query =request.session['privados']
        num=int(request.GET['privado'])-1
        query.pop(num);
        request.session['privados'] = query


    return query

def mccaadd_indicador(request):
    query = list()
    if(request.GET['tipo']=="add"):
        if("indicadores" in request.session):
            query =request.session['indicadores']
            num=len(query)+1
        else:
            num = 1
        query.extend([{'item':num,'indicador': request.GET['indicador']}])
        request.session['indicadores'] = query
    else:
        if("indicadores" in request.session):
            query =request.session['indicadores']
        num=int(request.GET['indicador'])-1
        query.pop(num);
        request.session['indicadores'] = query


    return query

def mccaadd_mensaje(request):
    query = list()
    if(request.GET['tipo']=="add"):
        if("mensajes" in request.session):
            query =request.session['mensajes']
            num=len(query)+1
        else:
            num = 1
        query.extend([{'item':num,'mensaje': request.GET['mensaje']}])
        request.session['mensajes'] = query
    else:
        if("mensajes" in request.session):
            query =request.session['mensajes']
        num=int(request.GET['mensaje'])-1
        query.pop(num);
        request.session['mensajes'] = query


    return query

def mccaadd_canal(request):
    query = list()
    if(request.GET['tipo']=="add"):
        if("canales" in request.session):
            query =request.session['canales']
            num=len(query)+1
        else:
            num = 1
        query.extend([{'item':num,'canal':request.GET['canal'] ,'tipommca_id':request.GET['tipocc']}])
        request.session['canales'] = query
    else:
        if("canales" in request.session):
            query =request.session['canales']
        num=int(request.GET['canal'])-1
        query.pop(num);
        request.session['canales'] = query

    return query

def mccaadd_accion(request):
    query = list()
    if(request.GET['tipo']=="add"):
        if("acciones" in request.session):
            query =request.session['acciones']
            num=len(query)+1
        else:
            num = 1
        query.extend([{'item':num,'accion':request.GET['accion'] ,'fechaini':request.GET['ini'],'fechafin':request.GET['fin']}])
        request.session['acciones'] = query
    else:
        if("acciones" in request.session):
            query =request.session['acciones']
        num=int(request.GET['accion'])-1
        query.pop(num);
        request.session['acciones'] = query

    return query


def mccaadd_observacion(request):
    query = list()
    if(request.GET['tipo']=="add"):
        if("observaciones" in request.session):
            query =request.session['observaciones']
            num=len(query)+1
        else:
            num = 1
        query.extend([{'item':num,'observacion': request.GET['obs']}])
        request.session['observaciones'] = query
    else:
        if("observaciones" in request.session):
            query =request.session['observaciones']
        num=int(request.GET['obs'])-1
        query.pop(num);
        request.session['observaciones'] = query


    return query

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

        if 'actor' in request.GET:
            query1 =mccadd_actor(request)

        if("actores" in request.session):
            query1 =request.session['actores']

        if 'lider' in request.GET:
            query2 =mccadd_lider(request)

        if("lideres" in request.session):
            query2 =request.session['lideres']

        if 'obs' in request.GET:
            query3 =mccadd_observacion(request)

        if("observaciones_mcc" in request.session):
            query3 =request.session['observaciones_mcc']
            
        config = RequestConfig(request)


        tabla1 = MccForm_ActorTable(query1)
        config.configure(tabla1)

        tabla2 = MccForm_LiderTable(query2)
        config.configure(tabla2)

        tabla3 = MccForm_ObservacionTable(query3)
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
