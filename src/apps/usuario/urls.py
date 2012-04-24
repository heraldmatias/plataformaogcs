# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('usuario.views',
    url(r'^add/$','useradd', name='ogcs-mantenimiento-usuario-add'),
    url(r'^edit/(?P<codigo>\d+)/$','useredit', name='ogcs-mantenimiento-usuario-edit'),
    url(r'^consulta/$','userquery', name='ogcs-mantenimiento-usuario-query'),
)
