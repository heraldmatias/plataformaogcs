# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('comunicacion.views',
    url(r'^oac/add/$','oacadd', name='ogcs-mantenimiento-oac-add'),
    url(r'^oac/consulta/$','oacquery', name='ogcs-mantenimiento-oac-query'),
    url(r'^pgcs/add/$','pgcsadd', name='ogcs-mantenimiento-pgcs-add'),
    url(r'^pgcs/consulta/$','pgcsquery', name='ogcs-mantenimiento-pgcs-query'),
    url(r'^pgcs/aporte/add/$','pgcs_apor_add', name='ogcs-mantenimiento-pgcs-aporte-add'),
    url(r'^pgcs/aporte/consulta/$','pgcs_apor_query', name='ogcs-mantenimiento-pgcs-aporte-query'),
)
