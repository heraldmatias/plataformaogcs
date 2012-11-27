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
from dependencia.models import Odp, Ministerio, Gobernacion
from datetime import datetime
from django.conf import settings
from calendario import calendar
from calendario.forms import CalendarConsultaForm

def _get_dependencia(organismo_id, dependencia_id):
    ini = None
    try:
        if organismo_id == '1':
            ini = Ministerio.objects.get(nummin=dependencia_id)
        elif organismo_id == '2':
            ini = Odp.objects.get(numodp=dependencia_id)
        elif organismo_id == '3':
            ini = Gobernacion.objects.get(numgob=dependencia_id)
    except:
        pass
    return ini

def internal_error_view(request):
    return render_to_response('500.html',{},context_instance=RequestContext(request))
def index(request):
    form = LoginForm()
    if 'next' in request.GET:
        return render_to_response('home/index.html', {'form': form,
            'login':'login','permission':False}, 
            context_instance=RequestContext(request),)
    return render_to_response('home/index.html', {'form': form,
        'login':'login'}, context_instance=RequestContext(request),)

@login_required()
def view_calendar(request):
    form = CalendarConsultaForm(request.GET)
    dependencia_id = request.GET.get('dependencia')
    organismo_id = request.GET.get('organismo')
    dependencia = _get_dependencia(organismo_id,dependencia_id)
    frame = (dependencia is None) and calendar.getinframe() or calendar.getinframe(dependencia)
    return render_to_response('home/calendario.html',
    {'frame':frame,    
    'form':form,'dependencia':dependencia_id,},
     context_instance=RequestContext(request),)

@login_required()
def permission_denied(request):
    return render_to_response('home/permiso_denegado.html', context_instance=RequestContext(request),)

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
            request.session['login_date'] = today
            usuario = Usuario.objects.get(user=request.user)
            request.session['nombres'] = usuario.nombres
            if profile.organismo.codigo == 1:
                ini = Ministerio.objects.get(nummin=profile.dependencia)
            elif profile.organismo.codigo == 2:
                ini = Odp.objects.get(numodp=profile.dependencia)
            elif profile.organismo.codigo == 3:
                ini = Gobernacion.objects.get(numgob=profile.dependencia)
            request.session['dependencia'] = ini            
            return redirect('ogcs-index')
        else:    
            form = LoginForm()
            return render(request,
                        "home/index.html",
                        {"error_message":"Su cuenta esta inactiva, porfavor consulte con su Administrador.",'form':form,'login':'login'})
    else:
        form = LoginForm()
        return render(request,
                        "home/index.html",
                        {"error_message":"Por favor ingrese valores correctos.",'form':form,'login':'login'})

@login_required()
def main(request): 
    if 'm' in request.GET:
        return render_to_response('home/home.html',{'m':request.GET['m']}, context_instance=RequestContext(request),)
    else: 
        return render_to_response('home/home.html', context_instance=RequestContext(request),)

@login_required()
def singout(request):
    logout(request)
    return redirect(settings.LOGIN_URL)

