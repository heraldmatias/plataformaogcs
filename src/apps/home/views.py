# -*- coding: utf-8 -*-
from django.shortcuts import render, render_to_response, redirect
from forms import LoginForm
#from ubigeo.forms import RegionForm, ProvinciaForm
#from dependencia.forms import MinisterioForm, OdpForm, GobernacionForm
#from redessociales.forms import InformacionForm, TwitterForm, FacebookForm, TwitterDiarioForm, FacebookDiarioForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from usuario.models import Usuario
from datetime import datetime

def index(request):
    form = LoginForm()
    return render_to_response('home/index.html', {'form': form,}, context_instance=RequestContext(request),)

def singin(request):
    if request.method == 'POST':
        username = request.POST['usuario']
        password = request.POST['clave']
    try:
        profile = Usuario.objects.get(email=request.POST['usuario'])
        user = authenticate(username=profile.user.username, password=password)
    except:
        user = None
    if user is not None:
        if user.is_active:
            login(request, user)
            today = datetime.now() #fecha actual
            #dateFormat = today.strftime("%Y/%m/%d") # fecha con formato
            request.session['login_date'] = today
            nombres = Usuario.objects.get(user=request.user).nombres 
            request.session['nombres'] = nombres
            return redirect('/home/')
    else:
        form = LoginForm()
        return render(request,
                        "home/index.html",
                        {"error_message":"Por favor ingrese valores correctos.",'form':form,})

@login_required(login_url='/')
def main(request): 
    if 'm' in request.GET:
        return render_to_response('home/home.html',{'m':request.GET['m'],'usuario':request.session['nombres'],'fecha':request.session['login_date']}, context_instance=RequestContext(request),)
    else: 
        return render_to_response('home/home.html',{'usuario':request.session['nombres'],'fecha':request.session['login_date']}, context_instance=RequestContext(request),)

@login_required(login_url='/')
def singout(request):
    logout(request)
    return redirect('/')

