# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, redirect
from forms import UsuarioForm, UsuarioTable, ConsultaUsuarioForm
from django.template import RequestContext
from usuario.models import Usuario, Estado
from dependencia.models import Ministerio, Odp, Gobernacion
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
import django_tables2 as tables
from django_tables2.config import RequestConfig

@login_required(login_url='/')
def useradd(request):
    if request.method == 'POST':
        num = Usuario.objects.values("numero").order_by("-numero",)[:1]
        num = 1 if len(num)==0 else int(num[0]["numero"])+1
        frmusuario = UsuarioForm(request.POST) # A form bound to the POST data
        if frmusuario.is_valid():
            if request.POST['organismo'] == "1":
                usernamee = Ministerio.objects.get(nummin=request.POST['dependencia']).iniciales+"0"+request.POST['organismo']+"0"+request.POST['dependencia']
            elif request.POST['organismo'] == "2":
                usernamee = Odp.objects.get(numodp=request.POST['dependencia']).iniciales+"0"+request.POST['organismo']+"0"+request.POST['dependencia']                
            elif request.POST['organismo'] == "3":
                usernamee = Gobernacion.objects.get(numgob=request.POST['dependencia']).iniciales+"0"+request.POST['organismo']+"0"+request.POST['dependencia']
            user = User.objects.create_user(username=usernamee,email=request.POST['email'],password=request.POST['contrasena'])
            if request.POST['nivel'] == "2":
                user.is_staff = True
                user.is_superuser = True
            if request.POST['estado'] == "2":
                user.is_active = False
            user.save()
            usuario = Usuario(user=user,numero=num)
            frmusuario = UsuarioForm(request.POST, instance=usuario)
            frmusuario.save()
            asunto="Bienvenido a la plataforma de Comunicacion Social"
            mensaje =u"""Desde este momento usted puede usar la Plataforma Intersectorial de Redes Sociales OGCS - PCM. Le adjuntamos su USUARIO Y CONTRASEÑA con el cual podrá acceder a la Plataforma.
		USUARIO: %s
		CONTRASEÑA: %s
            """ % (user.email, request.POST['contrasena'])
            #mails = [user.email,]
	    try:
	        #send_mail(asunto, mensaje, 'heraldmatias.oz@gmail.com', mails)
                user.email_user(subject=asunto, message=mensaje)
            except:
                return redirect('/home/?m=userr',)
            return redirect('/home/?m=usadd',)
    else:        
        frmusuario = UsuarioForm()
    return render_to_response('usuario/usuario.html', {'frmusuario': frmusuario,'opcion':'add','usuario':request.session['nombres'],'fecha':request.session['login_date']}, context_instance=RequestContext(request),)

@login_required(login_url='/')
def useredit(request, codigo):
    if request.method == 'POST':
        profile = Usuario.objects.get(user = request.user)
        usuario = Usuario.objects.get(numero=int(codigo))
        usuario.idusuario_mod=profile.numero
        frmusuario = UsuarioForm(request.POST, instance=usuario) # A form bound to the POST data	
        if frmusuario.is_valid():
            frmusuario.save()
            return redirect('/home/') # Crear un parametro en home para mostrar los mensajes de exito.
    else:
        usuario = get_object_or_404(Usuario, numero=int(codigo))
        frmusuario = UsuarioForm(instance=usuario)
    return render_to_response('usuario/usuario.html', {'frmusuario': frmusuario,'opcion':'edit','codigo':codigo,'usuario':request.session['nombres'],'fecha':request.session['login_date']}, context_instance=RequestContext(request),)

@login_required(login_url='/')
def userquery(request):
    col = "-nombres"
    if "2-sort" in request.GET:
        col = request.GET['2-sort']
    usuarios = Usuario.objects.all()
    config = RequestConfig(request)
    if request.method == "POST":
        consultausuarioform = ConsultaUsuarioForm(request.POST)        
        if consultausuarioform.is_valid():
            usuarios = usuarios.filter(nombres__icontains=request.POST['nombres']).order_by(col)
    else:
        consultausuarioform = ConsultaUsuarioForm()
    tblusuarios = UsuarioTable(usuarios.order_by(col))
    config.configure(tblusuarios)
    tblusuarios.paginate(page=request.GET.get('page', 1), per_page=6)
    return render_to_response('usuario/usuario_consulta.html', {'consultausuarioform':consultausuarioform,'tabla':tblusuarios,'usuario':request.session['nombres'],'fecha':request.session['login_date']}, context_instance=RequestContext(request),)

