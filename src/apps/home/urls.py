# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url
from django.contrib.auth.views import password_reset, password_reset_done,password_reset_confirm,password_reset_complete

urlpatterns = patterns('home.views',
    url(r'^$','main', name='ogcs-index'),
    url(r'^login/$','singin', name='ogcs-login'),    
    url(r'^logout/$','singout', name='ogcs-logout'),
    url(r'^accounts/password/reset/$', password_reset,{'template_name':'home/cambiar_clave.html','extra_context':{'login':'login'}},name='ogcs-reset-pass'),
    url(r'^accounts/password/reset/done/$', password_reset_done,{'template_name':'home/cambiar_clave_hecho.html','extra_context':{'login':'login',}} ,name='ogcs-reset-done'),
    url(r'^accounts/password/reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', password_reset_confirm,name='ogcs-reset-confirm'),
    url(r'^accounts/password/done/$', password_reset_complete,name='ogcs-reset-complete'),
)
