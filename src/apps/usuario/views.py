# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, redirect
from forms import UsuarioForm, UsuarioTable, ConsultaUsuarioForm,EditUsuarioForm 
from django.template import RequestContext
from usuario.models import Usuario, Estado, Organismo, Nivel
from dependencia.models import Ministerio, Odp, Gobernacion
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
import django_tables2 as tables
from django_tables2.config import RequestConfig
from datetime import datetime
from scripts.scripts import imprimirToExcel
from django.core.urlresolvers import reverse

serie = 3

@login_required()
@permission_required('usuario.add_usuario')
def useradd(request,nivel):
    existe = -1
    if request.method == 'POST':
        num = Usuario.objects.values("numero").order_by("-numero",)[:1]
        num = 1 if len(num)==0 else int(num[0]["numero"])+1
        frmusuario = UsuarioForm(request.POST) 
        if frmusuario.is_valid():
            if request.POST['nivel'] == "1":
                try:
                    obj = Usuario.objects.get(organismo = Organismo.objects.get(codigo=request.POST['organismo']), dependencia=request.POST['dependencia'])
                    existe = 0
                except:
                    existe = 1
            elif request.POST['organismo'] == "1" and request.POST['dependencia'] == "1":
                existe = 2
            else:
                existe = 3
            if existe == 1 or existe == 2:
                if request.POST['organismo'] == "1":
                    usernamee = Ministerio.objects.get(nummin=request.POST['dependencia']).iniciales+(serie-len(str(num)))*'0'+str(num)
                elif request.POST['organismo'] == "2":
                    usernamee = Odp.objects.get(numodp=request.POST['dependencia']).iniciales+(serie-len(str(num)))*'0'+str(num)
                elif request.POST['organismo'] == "3":
                    usernamee = Gobernacion.objects.get(numgob=request.POST['dependencia']).iniciales+(serie-len(str(num)))*'0'+str(num)
                user = User.objects.create_user(username=usernamee,email=request.POST['email'],password=request.POST['contrasena'],)
                if request.POST['nivel'] == "2":
                    user.is_staff = True
                    user.is_superuser = True
                if request.POST['estado'] == "2":
                    user.is_active = False
                user.first_name = request.POST['nombres']
                user.last_name = request.POST['apellidos']
                user.save()
                usuario = Usuario(user=user,numero=num,usuario=usernamee,nivel=Nivel.objects.get(codigo=request.POST['nivel']))
                frmusuario = UsuarioForm(request.POST,request.FILES, instance=usuario)
                frmusuario.save()
                usuario.contrasena = user.password
                usuario.save() 
                asunto="Bienvenido a la plataforma de Comunicacion Social"
                mensaje =u"""Desde este momento usted puede usar la Plataforma Intersectorial de Redes Sociales OGCS - PCM. Le adjuntamos su USUARIO Y CONTRASEÑA con el cual podrá acceder a la Plataforma.
		USUARIO: %s
		CONTRASEÑA: %s
            """ % (user.email, request.POST['contrasena'])
	        try:
	        #send_mail(asunto, mensaje, 'heraldmatias.oz@gmail.com', mails)
                    user.email_user(subject=asunto, message=mensaje)
                except:
                    return redirect(reverse('ogcs-index')+'?m=userr')
                return redirect(reverse('ogcs-index')+'?m=usadd')
    else:        
        frmusuario = UsuarioForm()
    return render_to_response('usuario/usuario.html', {'frmusuario': frmusuario,'opcion':'add','existe':existe,'nivel':nivel,'dependencia': request.POST['dependencia'] if 'dependencia' in request.POST else 0,}, context_instance=RequestContext(request),)

@login_required()
@permission_required('usuario.change_usuario')
def useredit(request,nivel, codigo):
    if request.method == 'POST':
        profile = Usuario.objects.get(user = request.user)
        usuario = Usuario.objects.get(numero=int(codigo))
        usuario.idusuario_mod=profile.numero
        frmusuario = EditUsuarioForm(request.POST,request.FILES, instance=usuario) 
        dependencia = request.POST['dependencia']
        if frmusuario.is_valid():
            usuario.user.is_active= 0 if request.POST['estado']=="2" else 1
            usuario.user.last_name = request.POST['apellidos']
            usuario.user.first_name = request.POST['nombres']
            #usuario.user.set_password = request.POST['contrasena']
            usuario.user.save()
            frmusuario.save()
            return redirect(reverse('ogcs-mantenimiento-usuario-consulta',kwargs={'nivel':nivel})+'?m=edit')
    else:
        usuario = get_object_or_404(Usuario, numero=int(codigo))
        dependencia = usuario.dependencia
        frmusuario = EditUsuarioForm(instance=usuario)
    return render_to_response('usuario/usuario.html', {'frmusuario': frmusuario,'opcion':'edit','codigo':codigo,'dependencia':dependencia,'nivel':nivel,}, context_instance=RequestContext(request),)

@login_required()
@permission_required('usuario.query_usuario')
def userquery(request, nivel):
    col = "-nombres"
    if "2-sort" in request.GET:
        col = request.GET['2-sort']
    config = RequestConfig(request)
    consultausuarioform = ConsultaUsuarioForm(request.GET)
    filtro = list()
    usuarios = None
    dependencia=0
    if ('nombres' in request.GET and 'organismo' in request.GET and 'estado' in request.GET and 'apellidos' in request.GET) or 'dependencia' in request.GET:
        if request.GET['nombres']:
            usuarios = Usuario.objects.filter(nombres__icontains=request.GET['nombres'])
        if request.GET['organismo']:
            filtro.append(u"organismo_id =%s"%request.GET['organismo'])
        if request.GET['estado']:
            filtro.append(u"estado_id =%s"%request.GET['estado'])
        if request.GET['apellidos']:
            if usuarios:
                usuarios = usuarios.filter(apellidos__icontains=request.GET['apellidos'])
            else:
                usuarios = Usuario.objects.filter(apellidos__icontains=request.GET['apellidos'])
        if 'dependencia' in request.GET:
            if request.GET['dependencia']:
                filtro.append(u"dependencia =%s"%request.GET['dependencia'])
                dependencia=request.GET['dependencia']
    else:
        usuarios = Usuario.objects.all()
    filtro.append(u'numero >0')
    filtro.append(u'nivel_id = '+nivel)
    if usuarios is None:
        usuarios = Usuario.objects.extra(where=filtro)
    else:
        usuarios = usuarios.extra(where=filtro)
    usuarios = usuarios.extra(select={'dependencia':"case organismo_id when 1 then (select ministerio from ministerio where nummin=dependencia) when 2 then (select odp from odp where numodp=dependencia) when 3 then (select gobernacion from gobernacion where numgob=dependencia) end"})
    tblusuarios = UsuarioTable(usuarios.order_by(col))
    config.configure(tblusuarios)
    tblusuarios.paginate(page=request.GET.get('page', 1), per_page=6)
    return render_to_response('usuario/usuario_consulta.html', {'consultausuarioform':consultausuarioform,'tabla':tblusuarios,'dependencia':dependencia,'nivel':nivel,'mensaje':(request.GET['m'] if 'm' in request.GET else '')}, context_instance=RequestContext(request),)

@login_required()
@permission_required('usuario.query_usuario')
def userprint(request, nivel):
    filtro=list()
    usuarios = None
    dependencia=0
    if ('nombres' in request.GET and 'organismo' in request.GET and 'estado' in request.GET and 'apellidos' in request.GET) or 'dependencia' in request.GET:
        if request.GET['nombres']:
            usuarios = Usuario.objects.filter(nombres__icontains=request.GET['nombres'])
        if request.GET['organismo']:
            filtro.append(u"organismo_id =%s"%request.GET['organismo'])
        if request.GET['estado']:
            filtro.append(u"estado_id =%s"%request.GET['estado'])
        if request.GET['apellidos']:
            if usuarios:
                usuarios = usuarios.filter(apellidos__icontains=request.GET['apellidos'])
            else:
                usuarios = Usuario.objects.filter(apellidos__icontains=request.GET['apellidos'])
        if 'dependencia' in request.GET:
            if request.GET['dependencia']:
                filtro.append(u"dependencia =%s"%request.GET['dependencia'])
                dependencia=request.GET['dependencia']
    else:
        usuarios = Usuario.objects.all()
    filtro.append(u'numero >0')
    filtro.append(u'nivel_id = '+nivel)
    if usuarios is None:
        usuarios = Usuario.objects.extra(where=filtro)
    else:
        usuarios = usuarios.extra(where=filtro)
    usuarios = usuarios.extra(select={'dependencia':"case organismo_id when 1 then (select ministerio from ministerio where nummin=dependencia) when 2 then (select odp from odp where numodp=dependencia) when 3 then (select gobernacion from gobernacion where numgob=dependencia) end"})
    filename= ("usuario" if nivel == "1" else "administrador")+"_%s.xls" % datetime.today().strftime("%Y%m%d")
    return imprimirToExcel('usuario/reporteusu.html', {'data': usuarios,'fecha':datetime.today().date(),'hora':datetime.today().time(),'usuario':request.session['nombres']},filename)
