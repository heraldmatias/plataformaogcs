# -*- coding: utf-8 -*-
from forms import *
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext
#from usuario.models import Usuario, Estado
from dependencia.models import Ministerio, Odp, Gobernacion
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
    return render_to_response('comunicacion/oac.html', {'formulario': formulario,'mensaje':mensaje,}, context_instance=RequestContext(request),)

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
    if request.user.get_profile().nivel.codigo == 2:
        if 'organismo' in request.GET:
            if request.GET['organismo']:
                filtro.append(u"oac.organismo_id =%s"%request.GET['organismo'])
        if 'dependencia' in request.GET:
            if request.GET['dependencia']:
                filtro.append(u"oac.dependencia =%s"%request.GET['dependencia'])
                dependencia=request.GET['dependencia']
    else:
        filtro.append(u"oac.organismo_id =%s"%request.user.get_profile().organismo.codigo)
        filtro.append(u"oac.dependencia =%s"%request.user.get_profile().dependencia) 
        filtro.append(u"idusuario_creac="+str(request.user.get_profile().numero))
    filtro.append(u"idusuario_creac=usuario.numero")
    query = Oac.objects.extra(tables=['usuario',],where=filtro,select={'usuario':'usuario.usuario','dependencia':"case oac.organismo_id when 1 then (select ministerio from ministerio where nummin=oac.dependencia) when 2 then (select odp from odp where numodp=oac.dependencia) when 3 then (select gobernacion from gobernacion where numgob=oac.dependencia) end"})
    tabla = OacTable(query.order_by(col))
    config.configure(tabla)
    tabla.paginate(page=request.GET.get('page', 1), per_page=6)
    return render_to_response('comunicacion/oac_consulta.html', {'formulario':formulario,'tabla':tabla,'dependencia':dependencia,}, context_instance=RequestContext(request),)

@login_required()
def oacprint(request):
    filtro = list()
    if request.user.get_profile().nivel.codigo == 2:
        if 'organismo' in request.GET:
            if request.GET['organismo']:
                filtro.append(u"oac.organismo_id =%s"%request.GET['organismo'])
        if 'dependencia' in request.GET:
            if request.GET['dependencia']:
                filtro.append(u"oac.dependencia =%s"%request.GET['dependencia'])
                dependencia=request.GET['dependencia']
    else:
        filtro.append(u"oac.organismo_id =%s"%request.user.get_profile().organismo.codigo)
        filtro.append(u"oac.dependencia =%s"%request.user.get_profile().dependencia)
        filtro.append(u"idusuario_creac="+str(request.user.get_profile().numero))
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
    return render_to_response('comunicacion/pgcs.html', {'formulario': formulario,'mensaje':mensaje,}, context_instance=RequestContext(request),)

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
    if request.user.get_profile().nivel.codigo == 2:
        if 'organismo' in request.GET:
            if request.GET['organismo']:
                filtro.append(u"pgcs.organismo_id =%s"%request.GET['organismo'])
        if 'dependencia' in request.GET:
            if request.GET['dependencia']:
                filtro.append(u"pgcs.dependencia =%s"%request.GET['dependencia'])
                dependencia=request.GET['dependencia']
    else:
        filtro.append(u"pgcs.organismo_id =%s"%request.user.get_profile().organismo.codigo)
        filtro.append(u"pgcs.dependencia =%s"%request.user.get_profile().dependencia)
        filtro.append(u"idusuario_creac="+str(request.user.get_profile().numero))
    filtro.append(u"idusuario_creac=usuario.numero")
    filtro.append(u"tipopgcs_id=1")
    query = Pgcs.objects.extra(tables=['usuario',],where=filtro,select={'usuario':'usuario.usuario','dependencia':"case pgcs.organismo_id when 1 then (select ministerio from ministerio where nummin=pgcs.dependencia) when 2 then (select odp from odp where numodp=pgcs.dependencia) when 3 then (select gobernacion from gobernacion where numgob=pgcs.dependencia) end"})
    tabla = PgcsTable(query.order_by(col))
    config.configure(tabla)
    tabla.paginate(page=request.GET.get('page', 1), per_page=6)
    return render_to_response('comunicacion/pgcs_consulta.html', {'formulario':formulario,'tabla':tabla,'dependencia':dependencia,}, context_instance=RequestContext(request),)

@login_required()
def pgcsprint(request,tipo):
    filtro = list()
    if request.user.get_profile().nivel.codigo == 2:
        if 'organismo' in request.GET:
            if request.GET['organismo']:
                filtro.append(u"pgcs.organismo_id =%s"%request.GET['organismo'])
        if 'dependencia' in request.GET:
            if request.GET['dependencia']:
                filtro.append(u"pgcs.dependencia =%s"%request.GET['dependencia'])
                dependencia=request.GET['dependencia']
    else:
        filtro.append(u"pgcs.organismo_id =%s"%request.user.get_profile().organismo.codigo)
        filtro.append(u"pgcs.dependencia =%s"%request.user.get_profile().dependencia)
        if tipo == 1: 
            filtro.append(u"idusuario_creac="+str(request.user.get_profile().numero))
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
            from dependencia.views import get_dependencia
            ini= get_dependencia(int(request.POST['organismo']),int(request.POST['dependencia']))
            archivo=request.FILES['archivo'].name
            filename= "PGCSAPORTE%s%s%s" % (ini.iniciales,datetime.today().strftime("%d%m%Y"),archivo[archivo.rfind('.'):])
            try:
                obj=Pgcs.objects.get(archivo='pgcs/'+filename)
            except:
                num = Pgcs.objects.values("numpgcs").order_by("-numpgcs",)[:1]
                num = 1 if len(num)==0 else int(num[0]["numpgcs"])+1
                obj = Pgcs(numpgcs=num,idusuario_creac=profile.numero,tipopgcs=TipoOgcs.objects.get(codigo=2))
            FileSystemStorage().delete('pgcs/'+filename)
            request.FILES['archivo'].name = filename
        formulario = PgcsAporteForm(request.POST,request.FILES,instance=obj ) # A form bound to the POST data
        if formulario.is_valid():
            formulario.save()
            obj.urlpgcs= obj.archivo.url
            obj.save()
            formulario = PgcsAporteForm() # Crear un parametro en home para mostrar los mensajes de exito.
            mensaje="Registro grabado satisfactoriamente."
    else:        
        formulario = PgcsAporteForm()
    return render_to_response('comunicacion/pgcs.html', {'formulario': formulario,'mensaje':mensaje,'aporte':'aporte',}, context_instance=RequestContext(request),)

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
    if request.user.get_profile().nivel.codigo == 2:
        if 'organismo' in request.GET:
            if request.GET['organismo']:
                filtro.append(u"pgcs.organismo_id =%s"%request.GET['organismo'])
        if 'dependencia' in request.GET:
            if request.GET['dependencia']:
                filtro.append(u"pgcs.dependencia =%s"%request.GET['dependencia'])
                dependencia=request.GET['dependencia']
    else:
        filtro.append(u"pgcs.organismo_id =%s"%request.user.get_profile().organismo.codigo)
        filtro.append(u"pgcs.dependencia =%s"%request.user.get_profile().dependencia)
        #filtro.append(u"idusuario_creac="+str(request.user.get_profile().numero))
    filtro.append(u"idusuario_creac=usuario.numero")
    filtro.append(u"tipopgcs_id=2")
    print filtro
    query = Pgcs.objects.extra(tables=['usuario',],where=filtro,select={'usuario':'usuario.usuario','dependencia':"case pgcs.organismo_id when 1 then (select ministerio from ministerio where nummin=pgcs.dependencia) when 2 then (select odp from odp where numodp=pgcs.dependencia) when 3 then (select gobernacion from gobernacion where numgob=pgcs.dependencia) end"})
    tabla = PgcsTable(query.order_by(col))
    config.configure(tabla)
    tabla.paginate(page=request.GET.get('page', 1), per_page=6)
    return render_to_response('comunicacion/pgcs_consulta.html', {'formulario':formulario,'tabla':tabla,'aporte':'aporte',}, context_instance=RequestContext(request),)

######################## MCCA INICIO ###############################################
####################################################################################

@login_required()
def mccaadd(request):
    mensaje = ""
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
        profile = request.user.get_profile()
        #ini=request.session['dependencia']
        num = Mcca.objects.values("nummcca").order_by("-nummcca",)[:1]
        num = 1 if len(num) == 0 else int(num[0]["nummcca"]) + 1
        fecini = request.POST["fechaini"]
        fecfin = request.POST["fechafin"]
        fecini = datetime.strptime(fecini, "%d/%m/%Y").strftime("%Y-%m-%d")
        fecfin = datetime.strptime(fecfin, "%d/%m/%Y").strftime("%Y-%m-%d")
        #obj = Mcca(nummcca=num, fechaini=fecini, fechafin=fecfin, organismo=1, dependencia=1, idusuario_creac=1, publico='ninguno')
        obj = Mcca(nummcca=num, fechaini=fecini,fechafin=fecfin,organismo=profile.organismo,dependencia=profile.dependencia,idusuario_creac=profile.numero,publico='ninguno')
        formmcca = MccaForm(request.POST, instance=obj)
		
        if formmcca.is_valid():
            formmcca.save()
        obj.save()
        #sectores_Estado_save
        for c in range(len(corg)):
            MccaEstado(nummcca=obj, item=c + 1, organismo=Organismo.objects.get(codigo=corg[c]), dependencia=cdep[c]).save()
        #sectores_privado_save
        for c in range(len(cpri)):
            MccaPrivado(nummcca=obj, item=c + 1, privado=cpri[c], auditoria=1).save()
        #indicadores_save
        for c in range(len(cind)):
            MccaIndicador(nummcca=obj, item=c + 1, indicador=cind[c], auditoria=1).save()
        #mensajes_save
        for c in range(len(cmen)):
            MccaMensaje(nummcca=obj, item=c + 1, mensaje=cmen[c], auditoria=1).save()
        #canales_save
        for c in range(len(ccan)):
            MccaCanal(nummcca=obj, item=c + 1, tipommca=MccaTipoComunicacion.objects.get(codigo=ctipo[c]), canal=ccan[c], auditoria=1).save()
        #acciones_save
        for c in range(len(cacc)):
            fecini1 = datetime.strptime(caccfini[c], "%d/%m/%Y").strftime("%Y-%m-%d")
            fecfin1 = datetime.strptime(caccffin[c], "%d/%m/%Y").strftime("%Y-%m-%d")
            MccaAccion(nummcca=obj, item=c + 1, fechainia=fecini1, fechafina=fecfin1, acciones=cacc[c], auditoria=1).save()
        #observaciones_save
        for c in range(len(cobs)):
            MccaObservacion(nummcca=obj, item=c + 1, observacion=cobs[c], auditoria=1).save()
        formmcca = MccaForm() # Crear un parametro en home para mostrar los mensajes de exito.
        mensaje = "Registro grabado satisfactoriamente."
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
    return render_to_response('comunicacion/mcca.html', {'form': formmcca, 'form_estado': formmcca_estado, 'form_privado': formmcca_privado, 'form_indicador': formmcca_indicador, 'form_mensaje': formmcca_mensaje, 'form_canal': formmcca_canal, 'form_accion': formmcca_accion, 'form_observacion': formmcca_observacion, 'tabla':tabla, 'tabla1':tabla1, 'tabla2':tabla2, 'tabla3':tabla3, 'tabla4':tabla4, 'tabla5':tabla5, 'tabla6':tabla6, 'mensaje':mensaje, 'accion': 'add'}, context_instance=RequestContext(request),)

@login_required()
def mccaedit(request, nummcca):
    mensaje = ""
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
        profile = request.user.get_profile()
        #ini=request.session['dependencia']
        fecini = request.POST["fechaini"]
        fecfin = request.POST["fechafin"]
        fecini = datetime.strptime(fecini, "%d/%m/%Y").strftime("%Y-%m-%d")
        fecfin = datetime.strptime(fecfin, "%d/%m/%Y").strftime("%Y-%m-%d")
        obj = Mcca.objects.get(nummcca=int(nummcca))
        obj.idusuario_mod=profile.numero
        formmcca = MccaForm(request.POST, instance=obj)
        if formmcca.is_valid():
            formmcca.save()
        obj.fechaini = fecini
        obj.fechafin = fecfin
        obj.save()
        #sectores_Estado_save
        query = MccaEstado.objects.filter(nummcca=obj)
        for c in range(len(corg)):
            try:
                row = MccaEstado.objects.get(nummcca=obj,item=c+1)
                row.organismo = Organismo.objects.get(codigo=corg[c])
                row.dependencia = cdep[c]
                row.save()
            except MccaEstado.DoesNotExist:
                MccaEstado(nummcca=obj, item=c+1, organismo=Organismo.objects.get(codigo=corg[c]), dependencia=cdep[c]).save()
        resto= len(corg)
        while resto < len(query):
            row = MccaEstado.objects.get(nummcca=obj,item=resto+1)
            row.delete()
            resto = resto + 1
            
        #sectores_privado_save
        query = MccaPrivado.objects.filter(nummcca=obj)
        for c in range(len(cpri)):
            try:
                row = MccaPrivado.objects.get(nummcca=obj,item=c+1)
                row.privado = cpri[c]
                row.save()
            except MccaPrivado.DoesNotExist:
                MccaPrivado(nummcca=obj, item=c+1, privado=cpri[c], auditoria=1).save()
        resto= len(cpri)
        while resto < len(query):
            row = MccaPrivado.objects.get(nummcca=obj,item=resto+1)
            row.delete()
            resto = resto + 1

        #indicadores_save
        query = MccaIndicador.objects.filter(nummcca=obj)
        for c in range(len(cind)):
            try:
                row = MccaIndicador.objects.get(nummcca=obj,item=c+1)
                row.indicador = cind[c]
                row.save()
            except MccaIndicador.DoesNotExist:
                MccaIndicador(nummcca=obj, item=c+1, indicador=cind[c], auditoria=1).save()
        resto= len(cind)
        while resto < len(query):
            row = MccaIndicador.objects.get(nummcca=obj,item=resto+1)
            row.delete()
            resto = resto + 1

       #mensajes_save
        query = MccaMensaje.objects.filter(nummcca=obj)
        for c in range(len(cmen)):
            try:
                row = MccaMensaje.objects.get(nummcca=obj,item=c+1)
                row.mensaje = cmen[c]
                row.save()
            except MccaMensaje.DoesNotExist:
                MccaMensaje(nummcca=obj, item=c+1, mensaje=cmen[c], auditoria=1).save()
        resto= len(cmen)
        while resto < len(query):
            row = MccaMensaje.objects.get(nummcca=obj,item=resto+1)
            row.delete()
            resto = resto + 1

        #canales_save
        query = MccaCanal.objects.filter(nummcca=obj)
        for c in range(len(ccan)):
            try:
                row = MccaCanal.objects.get(nummcca=obj,item=c+1)
                row.tipommca=MccaTipoComunicacion.objects.get(codigo=ctipo[c])
                row.canal=ccan[c]
                row.save()
            except MccaCanal.DoesNotExist:
                MccaCanal(nummcca=obj, item=c+1, tipommca=MccaTipoComunicacion.objects.get(codigo=ctipo[c]), canal=ccan[c], auditoria=1).save()
        resto= len(ccan)
        while resto < len(query):
            row = MccaCanal.objects.get(nummcca=obj,item=resto+1)
            row.delete()
            resto = resto + 1

        #acciones_save
        query = MccaAccion.objects.filter(nummcca=obj)
        for c in range(len(cacc)):
            fecini1 = datetime.strptime(caccfini[c], "%d/%m/%Y").strftime("%Y-%m-%d")
            fecfin1 = datetime.strptime(caccffin[c], "%d/%m/%Y").strftime("%Y-%m-%d")
            try:
                row = MccaAccion.objects.get(nummcca=obj,item=c+1)
                row.fechainia=fecini1
                row.fechafina=fecfin1
                row.acciones=cacc[c]
                row.save()
            except MccaAccion.DoesNotExist:
                MccaAccion(nummcca=obj, item=c+1, fechainia=fecini1, fechafina=fecfin1, acciones=cacc[c], auditoria=1).save()
        resto= len(cacc)
        while resto < len(query):
            row = MccaAccion.objects.get(nummcca=obj,item=resto+1)
            row.delete()
            resto = resto + 1

        #observaciones_save
        query = MccaObservacion.objects.filter(nummcca=obj)
        for c in range(len(cobs)):
            try:
                row = MccaObservacion.objects.get(nummcca=obj,item=c+1)
                row.observacion = cobs[c]
                row.save()
            except MccaObservacion.DoesNotExist:
                MccaObservacion(nummcca=obj, item=c+1, observacion=cobs[c], auditoria=1).save()
        resto= len(cobs)
        while resto < len(query):
            row = MccaObservacion.objects.get(nummcca=obj,item=resto+1)
            row.delete()
            resto = resto + 1
            
        mensaje = "Registro modificado satisfactoriamente."
   
    mcca = get_object_or_404(Mcca, nummcca=int(nummcca))
    mcca.fechaini = mcca.fechaini.strftime("%d/%m/%Y")
    mcca.fechafin = mcca.fechafin.strftime("%d/%m/%Y")
    formmcca = MccaForm(instance=mcca)
    nomdependecia = ''
    query1 = MccaEstado.objects.filter(nummcca=mcca).order_by("item",)
    for row in query1:
        if row.organismo.codigo == 1:
            nomdependecia = Ministerio.objects.get(codigo=row.dependencia).ministerio
        if row.organismo.codigo == 2:
            nomdependecia = Odp.objects.get(codigo=row.dependencia).odp
        if row.organismo.codigo == 3:
            nomdependecia = Gobernacion.objects.get(codigo=row.dependencia).gobernacion
        row.nomdependecia = nomdependecia
    tabla = MccaForm_EstadoTable(query1)

    query2 = MccaPrivado.objects.filter(nummcca=mcca).order_by("item",)
    tabla1 = MccaForm_PrivadoTable(query2)

    query3 = MccaIndicador.objects.filter(nummcca=mcca).order_by("item",)
    tabla2 = MccaForm_IndicadorTable(query3)

    query4 = MccaMensaje.objects.filter(nummcca=mcca).order_by("item",)
    tabla3 = MccaForm_MensajeTable(query4)

    query5 = MccaCanal.objects.filter(nummcca=mcca).order_by("item",)
    tabla4 = MccaForm_CanalTable(query5)

    query6 = MccaAccion.objects.filter(nummcca=mcca).order_by("item",)
    for row in query6:
        row.fechainia = row.fechainia.strftime("%d/%m/%Y")
        row.fechafina = row.fechafina.strftime("%d/%m/%Y")
    tabla5 = MccaForm_AccionTable(query6)

    query7 = MccaObservacion.objects.filter(nummcca=mcca).order_by("item",)
    tabla6 = MccaForm_ObservacionTable(query7)
    
    formmcca_estado = MccaForm_Estado()
    formmcca_privado = MccaForm_Privado()
    formmcca_indicador = MccaForm_Indicador()
    formmcca_mensaje = MccaForm_Mensaje()
    formmcca_canal = MccaForm_Canal()
    formmcca_accion = MccaForm_Accion()
    formmcca_observacion = MccaForm_Observacion()
    return render_to_response('comunicacion/mcca.html', {'form': formmcca, 'form_estado': formmcca_estado, 'form_privado': formmcca_privado, 'form_indicador': formmcca_indicador, 'form_mensaje': formmcca_mensaje, 'form_canal': formmcca_canal, 'form_accion': formmcca_accion, 'form_observacion': formmcca_observacion, 'tabla':tabla, 'tabla1':tabla1, 'tabla2':tabla2, 'tabla3':tabla3, 'tabla4':tabla4, 'tabla5':tabla5, 'tabla6':tabla6, 'mensaje':mensaje, 'codigo':nummcca, 'accion': ''}, context_instance=RequestContext(request),)


@login_required()
def mcca_query(request):
    col = "-fechaini"
    query = None
    filtro = list()
    if "2-sort" in request.GET:
        col = request.GET['2-sort']
    config = RequestConfig(request)
    formulario = ConsultaMccaForm(request.GET)
    if request.user.get_profile().nivel.codigo == 2:
        if 'organismo' in request.GET:
            if request.GET['organismo']:
                filtro.append(u"mcca.organismo_id =%s" % request.GET['organismo'])
            if 'dependencia' in request.GET:
                if request.GET['dependencia']:
                    filtro.append(u"mcca.dependencia =%s" % request.GET['dependencia'])
                    dependencia = request.GET['dependencia']
    else:
        filtro.append(u"mcca.organismo_id =%s" % request.user.get_profile().organismo.codigo)  
        filtro.append(u"mcca.dependencia =%s" % request.user.get_profile().dependencia)  
        filtro.append(u"mcca.idusuario_creac=%s" % str(request.user.get_profile().numero))
    if 'nombremmca' in request.GET:
        if request.GET['nombremmca']:
            filtro.append(u"nombremmca = '%s'" % request.GET['nombremmca'])
    if 'fechaini' in request.GET:
        if request.GET['fechaini']:
            fecini = request.GET["fechaini"]
            fecini = datetime.strptime(fecini, "%d/%m/%Y").strftime("%Y-%m-%d")
            filtro.append(u"fechaini ='%s'" % fecini)
    if 'fechafin' in request.GET:
        if request.GET['fechafin']:
            fecfin = request.GET["fechafin"]
            fecfin = datetime.strptime(fecfin, "%d/%m/%Y").strftime("%Y-%m-%d")
            filtro.append(u"fechafin ='%s'" % fecfin)

    filtro.append(u"mcca.idusuario_creac=usuario.numero")
    query = Mcca.objects.extra(tables=['usuario',], where=filtro, select={'usuario':'usuario.usuario', 'idusuario_mod':'usuario.usuario', 'dependencia':"case mcca.organismo_id when 1 then (select ministerio from ministerio where nummin=mcca.dependencia) when 2 then (select odp from odp where numodp=mcca.dependencia) when 3 then (select gobernacion from gobernacion where numgob=mcca.dependencia) end"})
    #query = Mcca.objects.extra(where=filtro)
	#tabla = query.order_by(col)
    #return HttpResponse(serializers.serialize("json", tabla, ensure_ascii=False),mimetype='application/json')

    tabla = MccaTable(query.order_by(col))
    config.configure(tabla)
    tabla.paginate(page=request.GET.get('page', 1), per_page=6)
    return render_to_response('comunicacion/mcca_consulta.html', {'form':formulario, 'tabla':tabla}, context_instance=RequestContext(request),)

@login_required()
def mccaprint(request):
    col = "-fechaini"
    query = None
    filtro = list()
    if "2-sort" in request.GET:
        col = request.GET['2-sort']
    config = RequestConfig(request)
    formulario = ConsultaMccaForm(request.GET)
    if request.user.get_profile().nivel.codigo == 2:
        if 'organismo' in request.GET:
            if request.GET['organismo']:
                filtro.append(u"mcca.organismo_id =%s" % request.GET['organismo'])
            if 'dependencia' in request.GET:
                if request.GET['dependencia']:
                    filtro.append(u"mcca.dependencia =%s" % request.GET['dependencia'])
                    dependencia = request.GET['dependencia']
    else:
        filtro.append(u"mcca.organismo_id =%s" % request.user.get_profile().organismo.codigo)  
        filtro.append(u"mcca.dependencia =%s" % request.user.get_profile().dependencia)  
        filtro.append(u"mcca.idusuario_creac=%s" % str(request.user.get_profile().numero))
    if 'nombremmca' in request.GET:
        if request.GET['nombremmca']:
            filtro.append(u"nombremmca = '%s'" % request.GET['nombremmca'])
    if 'fechaini' in request.GET:
        if request.GET['fechaini']:
            fecini = request.GET["fechaini"]
            fecini = datetime.strptime(fecini, "%d/%m/%Y").strftime("%Y-%m-%d")
            filtro.append(u"fechaini ='%s'" % fecini)
    if 'fechafin' in request.GET:
        if request.GET['fechafin']:
            fecfin = request.GET["fechafin"]
            fecfin = datetime.strptime(fecfin, "%d/%m/%Y").strftime("%Y-%m-%d")
            filtro.append(u"fechafin ='%s'" % fecfin)

    filtro.append(u"mcca.idusuario_creac=usuario.numero")    
    query = Mcca.objects.extra(tables=['usuario',], where=filtro, select={'usuario':'usuario.usuario', 'idusuario_mod':'usuario.usuario', 'dependencia':"case mcca.organismo_id when 1 then (select ministerio from ministerio where nummin=mcca.dependencia) when 2 then (select odp from odp where numodp=mcca.dependencia) when 3 then (select gobernacion from gobernacion where numgob=mcca.dependencia) end"})
    #query = Mcca.objects.extra(where=filtro)
	#tabla = query.order_by(col)
    #return HttpResponse(serializers.serialize("json", tabla, ensure_ascii=False),mimetype='application/json')
    query = query.order_by(col)
		
    filename = ("mcca_%s.csv") % datetime.today().strftime("%Y%m%d")
    return imprimirToExcel('comunicacion/reporte_mcca.html', {'data': query, 'fecha':datetime.today().date(), 'hora':datetime.today().time(), 'usuario':'nombre'}, filename)

######################## MCCA FINAL ################################################
####################################################################################


######################## MCC INICIO ###############################################
####################################################################################

@login_required()
def mccadd(request):
    mensaje = ""
    if request.method == 'POST':
        #actores
        numtvac = request.POST.getlist('numtvac')
        actores = request.POST.getlist('listactor')
        instac = request.POST.getlist('instac')
        #lideres
        numtvli = request.POST.getlist('numtvli')
        lideres = request.POST.getlist('listlider')
        instli = request.POST.getlist('instli')
        #observaciones
        cobs = request.POST.getlist('cobs')
		
        num = Mcc.objects.values("nummcc").order_by("-nummcc",)[:1]
        num = 1 if len(num) == 0 else int(num[0]["nummcc"]) + 1
        fecini = request.POST["fechaini"]
        fecfin = request.POST["fechafin"]
        fecini = datetime.strptime(fecini, "%d/%m/%Y").strftime("%Y-%m-%d")
        fecfin = datetime.strptime(fecfin, "%d/%m/%Y").strftime("%Y-%m-%d")
        #obj = Mcc(nummcc=num, nombremmc=request.POST["nombremmc"], fechaini=fecini, fechafin=fecfin, organismo=1, dependencia=1, idusuario_creac=1)
        obj = Mcc(nummcc=num, nombremmc=request.POST["nombremmc"], fechaini=fecini, fechafin=fecfin,organismo=profile.organismo, dependencia=profile.dependencia, idusuario_creac=profile.numero)
        formmcc = MccForm(request.POST, instance=obj)
        if formmcc.is_valid():
            formmcc.save()
        obj.save()
        #actores_save
        for c in range(len(numtvac)):
            MccActor(nummcc=obj, item=c + 1, numtipovarios=MccTipoVarios.objects.get(codigo=numtvac[c]), actor=actores[c], institucion=instac[c], auditoria=1).save()
        #lideres_save
        for c in range(len(numtvli)):
            MccLider(nummcc=obj, item=c + 1, numtipovarios=MccTipoVarios.objects.get(codigo=numtvli[c]), lider=lideres[c], institucion=instli[c], auditoria=1).save()
        #observaciones_save
        for c in range(len(cobs)):
            MccObservacion(nummcc=obj, item=c + 1, observacion=cobs[c], auditoria=1).save()
        formmcca = MccForm() # Crear un parametro en home para mostrar los mensajes de exito.
				
        mensaje = "Registro grabado satisfactoriamente."
    
       
    tabla1 = MccForm_ActorTable(list())
    tabla2 = MccForm_LiderTable(list())
    tabla3 = MccForm_ObservacionTable(list())

    formmcc = MccForm()
    formmcc_lider = MccForm_Lider()
    formmcc_actor = MccForm_Actor()
    formmcc_observacion = MccForm_Observacion()

    return render_to_response('comunicacion/mcc.html', {'form': formmcc, 'form_actor': formmcc_actor, 'form_lider': formmcc_lider, 'form_observacion':formmcc_observacion, 'tabla1':tabla1, 'tabla2':tabla2, 'tabla3':tabla3, 'mensaje':mensaje, 'accion':'add'}, context_instance=RequestContext(request),)



@login_required()
def mccedit(request, nummcc):
    mensaje = ""
    if request.method == 'POST':
        #actores
        numtvac = request.POST.getlist('numtvac')
        actores = request.POST.getlist('listactor')
        instac = request.POST.getlist('instac')
        #lideres
        numtvli = request.POST.getlist('numtvli')
        lideres = request.POST.getlist('listlider')
        instli = request.POST.getlist('instli')
        #observaciones
        cobs = request.POST.getlist('cobs')

        profile = request.user.get_profile()
        fecini = request.POST["fechaini"]
        fecfin = request.POST["fechafin"]
        fecini = datetime.strptime(fecini, "%d/%m/%Y").strftime("%Y-%m-%d")
        fecfin = datetime.strptime(fecfin, "%d/%m/%Y").strftime("%Y-%m-%d")

        obj = Mcc.objects.get(nummcc=int(nummcc))
        obj.idusuario_mod=profile.numero
        
        formmcc = MccForm(request.POST, instance=obj)
        if formmcc.is_valid():
            formmcc.save()
        obj.fechaini = fecini
        obj.fechafin = fecfin
        obj.save()

        #actores_save
        query = MccActor.objects.filter(nummcc=obj)
        for c in range(len(actores)):
            try:
                row = MccActor.objects.get(nummcc=obj,item=c+1)
                row.numtipovarios=MccTipoVarios.objects.get(codigo=numtvac[c])
                row.actor=actores[c]
                row.institucion=instac[c]
                row.save()
            except MccActor.DoesNotExist:
                MccActor(nummcc=obj, item=c+1, numtipovarios=MccTipoVarios.objects.get(codigo=numtvac[c]), actor=actores[c], institucion=instac[c], auditoria=1).save()
        resto= len(actores)
        while resto < len(query):
            row = MccActor.objects.get(nummcc=obj,item=resto+1)
            row.delete()
            resto = resto + 1

        #lideres_save
        query = MccLider.objects.filter(nummcc=obj)
        for c in range(len(lideres)):
            try:
                row = MccLider.objects.get(nummcc=obj,item=c+1)
                row.numtipovarios=MccTipoVarios.objects.get(codigo=numtvli[c])
                row.lider=lideres[c]
                row.institucion=instli[c]
                row.save()
            except MccLider.DoesNotExist:
                MccLider(nummcc=obj, item=c+1, numtipovarios=MccTipoVarios.objects.get(codigo=numtvli[c]), lider=lideres[c], institucion=instli[c], auditoria=1).save()
        resto= len(lideres)
        while resto < len(query):
            row = MccLider.objects.get(nummcc=obj,item=resto+1)
            row.delete()
            resto = resto + 1

        #observaciones_save
        query = MccObservacion.objects.filter(nummcc=obj)
        for c in range(len(cobs)):
            try:
                row = MccObservacion.objects.get(nummcc=obj,item=c+1)
                row.observacion = cobs[c]
                row.save()
            except MccObservacion.DoesNotExist:
                MccObservacion(nummcc=obj, item=c+1, observacion=cobs[c], auditoria=1).save()
        resto= len(cobs)
        while resto < len(query):
            row = MccObservacion.objects.get(nummcc=obj,item=resto+1)
            row.delete()
            resto = resto + 1

        mensaje = "Registro grabado satisfactoriamente."
    
       
    
    mcc = get_object_or_404(Mcc, nummcc=int(nummcc))
    mcc.fechaini = mcc.fechaini.strftime("%d/%m/%Y")
    mcc.fechafin = mcc.fechafin.strftime("%d/%m/%Y")
    formmcc = MccForm(instance=mcc)
	
    query1 = MccActor.objects.filter(nummcc=mcc).order_by("item",)
    tabla1 = MccForm_ActorTable(query1)
	
    query2 = MccLider.objects.filter(nummcc=mcc).order_by("item",)
    tabla2 = MccForm_LiderTable(query2)
    
	
    query3 = MccObservacion.objects.filter(nummcc=mcc).order_by("item",)
    tabla3 = MccForm_ObservacionTable(query3)

    formmcc_lider = MccForm_Lider()
    formmcc_actor = MccForm_Actor()
    formmcc_observacion = MccForm_Observacion()

    return render_to_response('comunicacion/mcc.html', {'form': formmcc, 'form_actor': formmcc_actor, 'form_lider': formmcc_lider, 'form_observacion':formmcc_observacion, 'tabla1':tabla1, 'tabla2':tabla2, 'tabla3':tabla3, 'mensaje':mensaje, 'codigo':nummcc, 'accion': ''}, context_instance=RequestContext(request),)

@login_required()
def mcc_query(request):
    col = "-fechaini"
    query = list()
    filtro = list()
    if "2-sort" in request.GET:
        col = request.GET['2-sort']
    config = RequestConfig(request)
    form = ConsultaMccForm(request.GET)
    if 'organismo' in request.GET:
        if request.GET['organismo']:
            filtro.append(u"mcc.organismo_id =%s" % request.GET['organismo'])
        if 'dependencia' in request.GET:
            if request.GET['dependencia']:
                filtro.append(u"mcc.dependencia =%s" % request.GET['dependencia'])
    if 'nombremmc' in request.GET:
        if request.GET['nombremmc']:
            filtro.append(u"nombremmc like '%s'" % request.GET['nombremmc'])
    if 'fechaini' in request.GET:
        if request.GET['fechaini']:
            fecini = request.GET["fechaini"]
            fecini = datetime.strptime(fecini, "%d/%m/%Y").strftime("%Y-%m-%d")
            filtro.append(u"fechaini = '%s'" % fecini)
    if 'fechafin' in request.GET:
        if request.GET['fechafin']:
            fecfin = request.GET["fechafin"]
            fecfin = datetime.strptime(fecfin, "%d/%m/%Y").strftime("%Y-%m-%d")
            filtro.append(u"fechafin = '%s'" % fecfin)
    if 'nummcctipo' in request.GET:
        if request.GET['nummcctipo']:
            filtro.append(u"nummcctipo_id =%s" % request.GET['nummcctipo'])
    if 'nummccestado' in request.GET:
        if request.GET['nummccestado']:
            filtro.append(u"nummccestado_id =%s" % request.GET['nummccestado'])
    if 'region' in request.GET:
        if request.GET['region']:
            filtro.append(u"region_id =%s" % request.GET['region'])
        if 'provincia' in request.GET:
            if request.GET['provincia']:
                filtro.append(u"provincia_id =%s" % request.GET['provincia'])

    filtro.append(u"idusuario_creac=usuario.numero")
    #filtro.append(u"tipopgcs_id=2")
    query = Mcc.objects.extra(tables=['usuario',], where=filtro, select={'usuario':'usuario.usuario', 'idusuario_mod':'usuario.usuario', 'dependencia':"case mcc.organismo_id when 1 then (select ministerio from ministerio where nummin=mcc.dependencia) when 2 then (select odp from odp where numodp=mcc.dependencia) when 3 then (select gobernacion from gobernacion where numgob=mcc.dependencia) end"})
    #query = Mcc.objects.extra(where=filtro)
	#tabla = query.order_by(col)
    #return HttpResponse(serializers.serialize("json", tabla, ensure_ascii=False),mimetype='application/json')

    tabla = MccTable(query.order_by(col))
    config.configure(tabla)
    tabla.paginate(page=request.GET.get('page', 1), per_page=6)
    return render_to_response('comunicacion/mcc_consulta.html', {'form':form, 'tabla':tabla}, context_instance=RequestContext(request),)

@login_required()	
def mccprint(request):
    col = "-fechaini"
    query = list()
    filtro = list()
    if "2-sort" in request.GET:
        col = request.GET['2-sort']
    config = RequestConfig(request)
    form = ConsultaMccForm(request.GET)
    if 'organismo' in request.GET:
        if request.GET['organismo']:
            filtro.append(u"mcc.organismo_id =%s" % request.GET['organismo'])
        if 'dependencia' in request.GET:
            if request.GET['dependencia']:
                filtro.append(u"mcc.dependencia =%s" % request.GET['dependencia'])
    if 'nombremmc' in request.GET:
        if request.GET['nombremmc']:
            filtro.append(u"nombremmc like '%s'" % request.GET['nombremmc'])
    if 'fechaini' in request.GET:
        if request.GET['fechaini']:
            fecini = request.GET["fechaini"]
            fecini = datetime.strptime(fecini, "%d/%m/%Y").strftime("%Y-%m-%d")
            filtro.append(u"fechaini = '%s'" % fecini)
    if 'fechafin' in request.GET:
        if request.GET['fechafin']:
            fecfin = request.GET["fechafin"]
            fecfin = datetime.strptime(fecfin, "%d/%m/%Y").strftime("%Y-%m-%d")
            filtro.append(u"fechafin = '%s'" % fecfin)
    if 'nummcctipo' in request.GET:
        if request.GET['nummcctipo']:
            filtro.append(u"nummcctipo_id =%s" % request.GET['nummcctipo'])
    if 'nummccestado' in request.GET:
        if request.GET['nummccestado']:
            filtro.append(u"nummccestado_id =%s" % request.GET['nummccestado'])
    if 'region' in request.GET:
        if request.GET['region']:
            filtro.append(u"region_id =%s" % request.GET['region'])
        if 'provincia' in request.GET:
            if request.GET['provincia']:
                filtro.append(u"provincia_id =%s" % request.GET['provincia'])

    filtro.append(u"idusuario_creac=usuario.numero")
    #filtro.append(u"tipopgcs_id=2")
    query = Mcc.objects.extra(tables=['usuario',], where=filtro, select={'usuario':'usuario.usuario', 'idusuario_mod':'usuario.usuario', 'dependencia':"case mcc.organismo_id when 1 then (select ministerio from ministerio where nummin=mcc.dependencia) when 2 then (select odp from odp where numodp=mcc.dependencia) when 3 then (select gobernacion from gobernacion where numgob=mcc.dependencia) end"})
    #query = Mcc.objects.extra(where=filtro)
    #tabla = query.order_by(col)
    #return HttpResponse(serializers.serialize("json", tabla, ensure_ascii=False),mimetype='application/json')

    query = query.order_by(col)
		
    filename = ("mcc_%s.csv") % datetime.today().strftime("%Y%m%d")
    return imprimirToExcel('comunicacion/reporte_mcc.html', {'data': query, 'fecha':datetime.today().date(), 'hora':datetime.today().time(), 'usuario':'nombre'}, filename)

######################## MCC FINAL ################################################
####################################################################################
