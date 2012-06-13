# -*- coding: utf-8 -*-
from forms import *
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext
from models import MaterialGrafico, DocumentoInteresGeneral, ActaReunionIntersectorial, Documento
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.shortcuts import get_object_or_404
import django_tables2 as tables
from django_tables2.config import RequestConfig
from datetime import datetime
from scripts.scripts import imprimirToExcel
from django.http import HttpResponse, Http404
from django.core.files.storage import  FileSystemStorage
from usuario.models import Usuario
@login_required()
def mgadd(request):
    mensaje=""
    if request.method == 'POST':               
        if 'arcmg1' in request.FILES:
            profile = request.user.get_profile()
            ini=request.session['dependencia']            
            fss = FileSystemStorage()
            filename= "MG%s%s_01" % (ini.iniciales,datetime.today().strftime("%d%m%Y"))
            obj=MaterialGrafico.objects.extra(where=[u"SUBSTRING_INDEX(arcmg1, '.', 1) ='materialgrafico/"+filename+"'",])[:1]
            if len(obj)>0:
                dobj = obj.values('arcmg1','arcmg2','arcmg3','arcmg4','arcmg5','arcmg6','arcmg7','arcmg8')
                for a in range(1,9):
                    if dobj[0]['arcmg'+str(a)]:
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
                if obj.arcmg2:
                    obj.urlmg2= obj.arcmg2.url 
                if obj.arcmg3:
                    obj.urlmg3= obj.arcmg3.url
                if obj.arcmg4:
                    obj.urlmg4= obj.arcmg4.url
                if obj.arcmg5:
                    obj.urlmg5= obj.arcmg5.url
                if obj.arcmg6:
                    obj.urlmg6= obj.arcmg6.url
                if obj.arcmg7:
                    obj.urlmg7= obj.arcmg7.url
                if obj.arcmg8:
                    obj.urlmg8= obj.arcmg8.url                
                obj.save()
                mensaje="Registro grabado satisfactoriamente."
        formulario = MGForm() # Crear un parametro en home para mostrar los mensajes de exito.            
    else:        
        formulario = MGForm()
    return render_to_response('extras/mg.html', {'formulario': formulario,'mensaje':mensaje,}, context_instance=RequestContext(request),)

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
    if request.user.get_profile().nivel.codigo == 2:
        if 'organismo' in request.GET:
            if request.GET['organismo']:
                filtro.append(u"materialgrafico.organismo_id =%s"%request.GET['organismo'])
        if 'dependencia' in request.GET:
            if request.GET['dependencia']:
                filtro.append(u"materialgrafico.dependencia =%s"%request.GET['dependencia'])
                dependencia=request.GET['dependencia']
    else:
        filtro.append(u"materialgrafico.organismo_id =%s"%request.user.get_profile().organismo.codigo)
        filtro.append(u"materialgrafico.dependencia =%s"%request.user.get_profile().dependencia) 
        filtro.append(u"idusuario_creac="+str(request.user.get_profile().numero))
    filtro.append(u"idusuario_creac=usuario.numero")
    filtro.append(u"materialgrafico.organismo_id=organismo.codigo")
    try:
        query = MaterialGrafico.objects.extra(tables=['usuario','organismo'],where=filtro,select={'organismo':'organismo.nombre','usuario':'usuario.usuario','dependencia':"case materialgrafico.organismo_id when 1 then (select ministerio from ministerio where nummin=materialgrafico.dependencia) when 2 then (select odp from odp where numodp=materialgrafico.dependencia) when 3 then (select gobernacion from gobernacion where numgob=materialgrafico.dependencia) end",'tipo1':"SUBSTRING_INDEX(arcmg1, '.', -1)",'tipo2':"SUBSTRING_INDEX(arcmg2, '.', -1)",'tipo3':"SUBSTRING_INDEX(arcmg3, '.', -1)",'tipo4':"SUBSTRING_INDEX(arcmg4, '.', -1)",'tipo5':"SUBSTRING_INDEX(arcmg5, '.', -1)",'tipo6':"SUBSTRING_INDEX(arcmg6, '.', -1)",'tipo7':"SUBSTRING_INDEX(arcmg7, '.', -1)",'tipo8':"SUBSTRING_INDEX(arcmg8, '.', -1)"}).order_by(col).values('organismo','dependencia','fec_creac','usuario','dependencia','urlmg1','urlmg2','urlmg3','urlmg4','urlmg5','urlmg6','urlmg7','urlmg8','tipo1','tipo2','tipo3','tipo4','tipo5','tipo6','tipo7','tipo8')
        data = list()
        dmg = dict()     
        for mg in query:
            for a in range(1,9):
                if mg['urlmg'+str(a)]:
                    dmg = {'organismo':mg['organismo'],'dependencia':mg['dependencia'],'fec_creac':mg['fec_creac'],'usuario':mg['usuario'],'Descargar':mg['urlmg'+str(a)],'Tipo':mg['tipo'+str(a)]}
                    data.append(dmg)          
        tabla = MGTable(data)
        config.configure(tabla)
        tabla.paginate(page=request.GET.get('page', 1), per_page=6)
        return render_to_response('extras/mg_consulta.html', {'formulario':formulario,'tabla':tabla,'dependencia':dependencia,}, context_instance=RequestContext(request),)
    except:
        raise Http404

@login_required()
def mgprint(request):
    col = "-organismo"
    if "2-sort" in request.GET:
        col = request.GET['2-sort']
    filtro = list()
    if request.user.get_profile().nivel.codigo == 2:
        if 'organismo' in request.GET:
            if request.GET['organismo']:
                filtro.append(u"materialgrafico.organismo_id =%s"%request.GET['organismo'])
        if 'dependencia' in request.GET:
            if request.GET['dependencia']:
                filtro.append(u"materialgrafico.dependencia =%s"%request.GET['dependencia'])
                dependencia=request.GET['dependencia']
    else:
        filtro.append(u"materialgrafico.organismo_id =%s"%request.user.get_profile().organismo.codigo)
        filtro.append(u"materialgrafico.dependencia =%s"%request.user.get_profile().dependencia) 
        filtro.append(u"idusuario_creac="+str(request.user.get_profile().numero))
    filtro.append(u"idusuario_creac=usuario.numero")
    filtro.append(u"materialgrafico.organismo_id=organismo.codigo")
    query = MaterialGrafico.objects.extra(tables=['usuario','organismo'],where=filtro,select={'organismo':'organismo.nombre','usuario':'usuario.usuario','dependencia':"case materialgrafico.organismo_id when 1 then (select ministerio from ministerio where nummin=materialgrafico.dependencia) when 2 then (select odp from odp where numodp=materialgrafico.dependencia) when 3 then (select gobernacion from gobernacion where numgob=materialgrafico.dependencia) end",'tipo1':"SUBSTRING_INDEX(arcmg1, '.', -1)",'tipo2':"SUBSTRING_INDEX(arcmg2, '.', -1)",'tipo3':"SUBSTRING_INDEX(arcmg3, '.', -1)",'tipo4':"SUBSTRING_INDEX(arcmg4, '.', -1)",'tipo5':"SUBSTRING_INDEX(arcmg5, '.', -1)",'tipo6':"SUBSTRING_INDEX(arcmg6, '.', -1)",'tipo7':"SUBSTRING_INDEX(arcmg7, '.', -1)",'tipo8':"SUBSTRING_INDEX(arcmg8, '.', -1)"}).order_by(col).values('organismo','dependencia','fec_creac','usuario','dependencia','tipo1','tipo2','tipo3','tipo4','tipo5','tipo6','tipo7','tipo8')
    data = list()
    dmg = dict()     
    for mg in query:
        for a in range(1,9):
            if mg['tipo'+str(a)]:
                dmg = {'organismo':mg['organismo'],'dependencia':mg['dependencia'],'fecha':mg['fec_creac'],'usuario':mg['usuario'],'tipo':mg['tipo'+str(a)]}
                data.append(dmg)
    filename= "mg_%s.csv" % datetime.today().strftime("%Y%m%d")
    return imprimirToExcel('extras/reportemg.html', {'data': data,'fecha':datetime.today().date(),'hora':datetime.today().time(),'usuario':request.session['nombres']},filename)

@login_required()
def digadd(request):
    mensaje=""
    if request.method == 'POST':               
        if 'archmis1' in request.FILES and 'archaca1' in request.FILES and 'archbue1' in request.FILES:
            profile = request.user.get_profile()
            ini=request.session['dependencia']            
            fss = FileSystemStorage()
            filename= "DIG%s%s_01" % (ini.iniciales,datetime.today().strftime("%d%m%Y"))
            obj=DocumentoInteresGeneral.objects.extra(where=[u"SUBSTRING_INDEX(archmis1, '.', 1) ='documentosgeneral/mis/"+filename+"'",])[:1]
            if len(obj)>0:
                dobj = obj.values('archmis1','archmis2','archmis3','archaca1','archaca2','archaca3','archbue1','archbue2','archbue3')
                for ar in ('archmis','archaca','archbue'):
                    for a in range(1,4):
                        if dobj[0][ar+str(a)]:
                            fss.delete(dobj[0][ar+str(a)])
                obj = obj.get()
            else:    
                num = DocumentoInteresGeneral.objects.values("numdig").order_by("-numdig",)[:1]
                num = 1 if len(num)==0 else int(num[0]["numdig"])+1 
                obj = DocumentoInteresGeneral(numdig=num,organismo=profile.organismo,dependencia=profile.dependencia,idusuario_creac=profile.numero,)
            for archivo in request.FILES:   
                filename1 = request.FILES[archivo].name
                ext = filename1[filename1.rfind('.')+1:]
                filename= "DIG%s%s_0%s.%s" % (ini.iniciales,datetime.today().strftime("%d%m%Y"),archivo[-1:],ext.upper())                
                request.FILES[archivo].name = filename               
            formulario = DIGForm(request.POST,request.FILES,instance=obj ) # A form bound to the POST data
            if formulario.is_valid():
                formulario.save()
                obj.urlmis1= obj.archmis1.url
                if obj.archmis2:
                    obj.urlmis2= obj.archmis2.url
                if obj.archmis3:
                    obj.urlmis3= obj.archmis3.url                
                obj.urlaca1= obj.archaca1.url
                if obj.archaca2:
                    obj.urlaca2= obj.archaca2.url
                if obj.archaca3:
                    obj.urlaca3= obj.archaca3.url
                obj.urlbue1= obj.archbue1.url
                if obj.archbue2:
                    obj.urlbue2= obj.archbue2.url
                if obj.archbue3:
                    obj.urlbue3= obj.archbue3.url
                obj.save()
                mensaje="Registro grabado satisfactoriamente."
        formulario = DIGForm() # Crear un parametro en home para mostrar los mensajes de exito.            
    else:        
        formulario = DIGForm()
    return render_to_response('extras/dig.html', {'formulario': formulario,'mensaje':mensaje,}, context_instance=RequestContext(request),)

@login_required()
def digquery(request):
    col = "-organismo"
    query = None
    dependencia=''
    filtro = list()
    if "2-sort" in request.GET:
        col = request.GET['2-sort']
    config = RequestConfig(request)
    formulario = ConsultaDIGForm(request.GET)
    if request.user.get_profile().nivel.codigo == 2:
        if 'organismo' in request.GET:
            if request.GET['organismo']:
                filtro.append(u"documentointeresgeneral.organismo_id =%s"%request.GET['organismo'])
        if 'dependencia' in request.GET:
            if request.GET['dependencia']:
                filtro.append(u"documentointeresgeneral.dependencia =%s"%request.GET['dependencia'])
                dependencia=request.GET['dependencia']
    else:
        filtro.append(u"documentointeresgeneral.organismo_id =%s"%request.user.get_profile().organismo.codigo)
        filtro.append(u"documentointeresgeneral.dependencia =%s"%request.user.get_profile().dependencia) 
        filtro.append(u"idusuario_creac="+str(request.user.get_profile().numero))
    filtro.append(u"idusuario_creac=usuario.numero")
    filtro.append(u"documentointeresgeneral.organismo_id=organismo.codigo")
    try:
        query = DocumentoInteresGeneral.objects.extra(tables=['usuario','organismo'],where=filtro,select={'organismo':'organismo.nombre','usuario':'usuario.usuario','dependencia':"case documentointeresgeneral.organismo_id when 1 then (select ministerio from ministerio where nummin=documentointeresgeneral.dependencia) when 2 then (select odp from odp where numodp=documentointeresgeneral.dependencia) when 3 then (select gobernacion from gobernacion where numgob=documentointeresgeneral.dependencia) end",'tipomis1':"SUBSTRING_INDEX(archmis1, '.', -1)",'tipomis2':"SUBSTRING_INDEX(archmis2, '.', -1)",'tipomis3':"SUBSTRING_INDEX(archmis3, '.', -1)",'tipoaca1':"SUBSTRING_INDEX(archaca1, '.', -1)",'tipoaca2':"SUBSTRING_INDEX(archaca2, '.', -1)",'tipoaca3':"SUBSTRING_INDEX(archaca3, '.', -1)",'tipobue1':"SUBSTRING_INDEX(archbue1, '.', -1)",'tipobue2':"SUBSTRING_INDEX(archbue2, '.', -1)",'tipobue3':"SUBSTRING_INDEX(archbue3, '.', -1)"}).order_by(col).values('organismo','dependencia','fec_creac','usuario','dependencia','urlmis1','urlmis2','urlmis3','urlaca1','urlaca2','urlaca3','urlbue1','urlbue2','urlbue3','tipomis1','tipomis2','tipomis3','tipoaca1','tipoaca2','tipoaca3','tipobue1','tipobue2','tipobue3')
        data = list()
        dmg = dict()     
        for mg in query:
            for ar in ('mis','aca','bue'):
                for a in range(1,4):
                    if mg['url'+ar+str(a)]:
                        dmg = {'organismo':mg['organismo'],'dependencia':mg['dependencia'],'fec_creac':mg['fec_creac'],'usuario':mg['usuario'],'Descargar':mg['url'+ar+str(a)],'TipoArchivo':mg['tipo'+ar+str(a)],'Tipo':ar.upper()}
                        data.append(dmg)          
        tabla = DIGTable(data)
        config.configure(tabla)
        tabla.paginate(page=request.GET.get('page', 1), per_page=6)
        return render_to_response('extras/dig_consulta.html', {'formulario':formulario,'tabla':tabla,'dependencia':dependencia,}, context_instance=RequestContext(request),)
    except:
        raise Http404

@login_required()
def digprint(request):
    col = "-organismo"
    query = None
    dependencia=''
    filtro = list()
    if "2-sort" in request.GET:
        col = request.GET['2-sort']
    if request.user.get_profile().nivel.codigo == 2:
        if 'organismo' in request.GET:
            if request.GET['organismo']:
                filtro.append(u"documentointeresgeneral.organismo_id =%s"%request.GET['organismo'])
        if 'dependencia' in request.GET:
            if request.GET['dependencia']:
                filtro.append(u"documentointeresgeneral.dependencia =%s"%request.GET['dependencia'])
                dependencia=request.GET['dependencia']
    else:
        filtro.append(u"documentointeresgeneral.organismo_id =%s"%request.user.get_profile().organismo.codigo)
        filtro.append(u"documentointeresgeneral.dependencia =%s"%request.user.get_profile().dependencia) 
        filtro.append(u"idusuario_creac="+str(request.user.get_profile().numero))
    filtro.append(u"idusuario_creac=usuario.numero")
    filtro.append(u"documentointeresgeneral.organismo_id=organismo.codigo")
    query = DocumentoInteresGeneral.objects.extra(tables=['usuario','organismo'],where=filtro,select={'organismo':'organismo.nombre','usuario':'usuario.usuario','dependencia':"case documentointeresgeneral.organismo_id when 1 then (select ministerio from ministerio where nummin=documentointeresgeneral.dependencia) when 2 then (select odp from odp where numodp=documentointeresgeneral.dependencia) when 3 then (select gobernacion from gobernacion where numgob=documentointeresgeneral.dependencia) end",'tipomis1':"SUBSTRING_INDEX(archmis1, '.', -1)",'tipomis2':"SUBSTRING_INDEX(archmis2, '.', -1)",'tipomis3':"SUBSTRING_INDEX(archmis3, '.', -1)",'tipoaca1':"SUBSTRING_INDEX(archaca1, '.', -1)",'tipoaca2':"SUBSTRING_INDEX(archaca2, '.', -1)",'tipoaca3':"SUBSTRING_INDEX(archaca3, '.', -1)",'tipobue1':"SUBSTRING_INDEX(archbue1, '.', -1)",'tipobue2':"SUBSTRING_INDEX(archbue2, '.', -1)",'tipobue3':"SUBSTRING_INDEX(archbue3, '.', -1)"}).order_by(col).values('organismo','dependencia','fec_creac','usuario','dependencia','urlmis1','urlmis2','urlmis3','urlaca1','urlaca2','urlaca3','urlbue1','urlbue2','urlbue3','tipomis1','tipomis2','tipomis3','tipoaca1','tipoaca2','tipoaca3','tipobue1','tipobue2','tipobue3')
    data = list()
    dmg = dict()     
    for mg in query:
        for ar in ('mis','aca','bue'):
            for a in range(1,4):
                if mg['tipo'+ar+str(a)]:
                    dmg = {'organismo':mg['organismo'],'dependencia':mg['dependencia'],'fecha':mg['fec_creac'],'usuario':mg['usuario'],'tipoarchivo':mg['tipo'+ar+str(a)],'tipo':ar.upper()}
                    data.append(dmg)                  
    filename= "dig_%s.csv" % datetime.today().strftime("%Y%m%d")
    return imprimirToExcel('extras/reporte_dig.html', {'data': data,'fecha':datetime.today().date(),'hora':datetime.today().time(),'usuario':request.session['nombres']},filename)
    
@login_required()
def ariadd(request):
    mensaje=""
    if request.method == 'POST':               
        if 'archari' in request.FILES:
            profile = request.user.get_profile()
            ini=request.session['dependencia']      
            filename= "ARI%s%s.PDF" % (ini.iniciales,datetime.today().strftime("%d%m%Y"))
            try:
                obj=ActaReunionIntersectorial.objects.get(archari='actas/'+filename)
            except:
                num = ActaReunionIntersectorial.objects.values("numari").order_by("-numari",)[:1]
                num = 1 if len(num)==0 else int(num[0]["numari"])+1
                obj = ActaReunionIntersectorial(numari=num,organismo=profile.organismo,dependencia=profile.dependencia,idusuario_creac=profile.numero,)            
            request.FILES['archari'].name = filename            
        formulario = AriForm(request.POST,request.FILES,instance=obj ) 
        if formulario.is_valid():
            FileSystemStorage().delete('actas/'+filename)
            formulario.save()
            obj.urlari= obj.archari.url
            obj.save()
            formulario = AriForm() # Crear un parametro en home para mostrar los mensajes de exito.
            mensaje="Registro grabado satisfactoriamente."
    else:        
        formulario = AriForm()
    return render_to_response('extras/ari.html', {'formulario': formulario,'mensaje':mensaje}, context_instance=RequestContext(request),)


@login_required()
def ariquery(request):
    col = "-organismo"
    query = None
    dependencia=''
    filtro = list()
    if "2-sort" in request.GET:
        col = request.GET['2-sort']
    config = RequestConfig(request)
    formulario = ConsultaAriForm(request.GET)
    if request.user.get_profile().nivel.codigo == 2:
        if 'organismo' in request.GET:
            if request.GET['organismo']:
                filtro.append(u"actareunionintersectorial.organismo_id =%s"%request.GET['organismo'])
        if 'dependencia' in request.GET:
            if request.GET['dependencia']:
                filtro.append(u"actareunionintersectorial.dependencia =%s"%request.GET['dependencia'])
                dependencia=request.GET['dependencia']
    else:
        filtro.append(u"actareunionintersectorial.organismo_id =%s"%request.user.get_profile().organismo.codigo)
        filtro.append(u"actareunionintersectorial.dependencia =%s"%request.user.get_profile().dependencia) 
        filtro.append(u"idusuario_creac="+str(request.user.get_profile().numero))
    filtro.append(u"idusuario_creac=usuario.numero")
    query = ActaReunionIntersectorial.objects.extra(tables=['usuario',],where=filtro,select={'usuario':'usuario.usuario','dependencia':"case actareunionintersectorial.organismo_id when 1 then (select ministerio from ministerio where nummin=actareunionintersectorial.dependencia) when 2 then (select odp from odp where numodp=actareunionintersectorial.dependencia) when 3 then (select gobernacion from gobernacion where numgob=actareunionintersectorial.dependencia) end"}).filter(nombreari__icontains=request.GET['nombreari'] if 'nombreari' in request.GET else '')
    #if 'nombreari' in request.GET:
    #    query.filter(nombreari__icontains=request.GET['nombreari'])
    tabla = AriTable(query.order_by(col))
    config.configure(tabla)
    tabla.paginate(page=request.GET.get('page', 1), per_page=6)
    return render_to_response('extras/ari_consulta.html', {'formulario':formulario,'tabla':tabla,'dependencia':dependencia,}, context_instance=RequestContext(request),)

@login_required()
def ariprint(request):
    col = "-organismo"
    query = None
    filtro = list()
    if "2-sort" in request.GET:
        col = request.GET['2-sort']
    if request.user.get_profile().nivel.codigo == 2:
        if 'organismo' in request.GET:
            if request.GET['organismo']:
                filtro.append(u"actareunionintersectorial.organismo_id =%s"%request.GET['organismo'])
        if 'dependencia' in request.GET:
            if request.GET['dependencia']:
                filtro.append(u"actareunionintersectorial.dependencia =%s"%request.GET['dependencia'])
                dependencia=request.GET['dependencia']
    else:
        filtro.append(u"actareunionintersectorial.organismo_id =%s"%request.user.get_profile().organismo.codigo)
        filtro.append(u"actareunionintersectorial.dependencia =%s"%request.user.get_profile().dependencia) 
        filtro.append(u"idusuario_creac="+str(request.user.get_profile().numero))
    filtro.append(u"idusuario_creac=usuario.numero")
    query = ActaReunionIntersectorial.objects.extra(tables=['usuario',],where=filtro,select={'usuario':'usuario.usuario','dependencia':"case actareunionintersectorial.organismo_id when 1 then (select ministerio from ministerio where nummin=actareunionintersectorial.dependencia) when 2 then (select odp from odp where numodp=actareunionintersectorial.dependencia) when 3 then (select gobernacion from gobernacion where numgob=actareunionintersectorial.dependencia) end"}).filter(nombreari__icontains=request.GET['nombreari'] if 'nombreari' in request.GET else '')
    filename= "ari_%s.csv" % datetime.today().strftime("%Y%m%d")
    return imprimirToExcel('extras/reporte_ari.html', {'data': query,'fecha':datetime.today().date(),'hora':datetime.today().time(),'usuario':request.session['nombres']},filename)


def get_categoria(tipo):
   """
      Define la categoria del documento subido, VER campo estatico CATEGORIAS en models.py
   """
   categoria = 'OTROS'
   if tipo in ('JPG','GIF','ICO','PNG','TIF',):   
       categoria = 'IMAGENES'
   elif tipo in ('AVI','MOV','MP4','WMV','FLV','F4V','3GP'):   
       categoria = 'VIDEOS' 
   elif tipo in ('MP3','WAV','AMF','AMV'):
       categoria = 'AUDIOS'
   elif tipo in ('DOC','DOCX','PDF','PPT','PPTX','XLS','XLSX','TXT','ODT'):
       categoria = 'DOCUMENTOS'
   elif tipo in ('ZIP','TAR','GZ','ZIP','RAR','7Z',):
       categoria = 'COMPRIMIDOS'
   return categoria

@login_required()
def documentos_add(request):
    mensaje = ''
    if request.method == 'POST':
        if 'archivo' in request.FILES:
            profile = request.user.get_profile()
            archivo = request.FILES['archivo']
            extension = archivo.name[archivo.name.rfind('.')+1:].upper()
            obj = Documento(organismo=profile.organismo, dependencia=profile.dependencia,tipo= cat == 'OTROS' and 'OTRO' or extension,categoria=get_categoria(extension),idusuario_creac=profile)
            formulario = DocumentoForm(request.POST,request.FILES,instance=obj ) # A form bound to the POST data
            if formulario.is_valid():
                formulario.save()             
                obj.url_archivo=obj.archivo.url 
                obj.save()
                mensaje="Registro grabado satisfactoriamente."
        formulario = DocumentoForm()
    else:        
        formulario = DocumentoForm()
    return render_to_response('extras/documento.html', {'formulario': formulario,'mensaje':mensaje,}, context_instance=RequestContext(request),)

@login_required()
def documentos_query(request):
    col = "-organismo"
    query = None
    dependencia=''
    usuario = ''
    filtro = list()
    if "2-sort" in request.GET:
        col = request.GET['2-sort']
    config = RequestConfig(request)
    formulario = ConsultaDocumentoForm(request.GET)
    if 'organismo' in request.GET:
        if request.GET['organismo']:
            filtro.append(u"documentos.organismo_id =%s"%request.GET['organismo'])
        if 'dependencia' in request.GET:
            if request.GET['dependencia']:
                filtro.append(u"documentos.dependencia =%s"%request.GET['dependencia'])
                dependencia=request.GET['dependencia']
    if 'idusuario_creac' in request.GET:
        if request.GET['idusuario_creac']:
            filtro.append(u"idusuario_creac_id =%s"%request.GET['idusuario_creac'])
            usuario=request.GET['idusuario_creac']
    if 'categoria' in request.GET:
        if request.GET['categoria']:
            filtro.append(u"categoria =%s"%request.GET['categoria'])
    if 'tipo' in request.GET:
        if request.GET['organismo']:
            filtro.append(u"tipo =%s"%request.GET['tipo'])
    filtro.append(u"idusuario_creac_id=usuario.numero")
    query = Documento.objects.extra(tables=['usuario',],where=filtro,select={'usuario':'usuario.usuario','dependencia':"case documentos.organismo_id when 1 then (select ministerio from ministerio where nummin=documentos.dependencia) when 2 then (select odp from odp where numodp=documentos.dependencia) when 3 then (select gobernacion from gobernacion where numgob=documentos.dependencia) end"})
#.filter(nombreari__icontains=request.GET['nombreari'] if 'nombreari' in request.GET else '')
    tabla = DocumentoTable(query.order_by(col))
    config.configure(tabla)
    tabla.paginate(page=request.GET.get('page', 1), per_page=6)
    return render_to_response('extras/documento_consulta.html', {'formulario': formulario,'tabla':tabla,'dependencia':dependencia,'usuario':usuario}, context_instance=RequestContext(request),)

