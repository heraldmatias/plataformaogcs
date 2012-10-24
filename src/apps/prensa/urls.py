# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('prensa.views',   
    url(r'^rep/add/$','add_resumen_prensa', name='ogcs-mantenimiento-prensa-rep-add'),
    url(r'^rep/edit/(?P<codigo>\d+)/$','add_resumen_prensa', name='ogcs-mantenimiento-prensa-rep-edit'),
    url(r'^rep/consulta/$','query_resumen_prensa', name='ogcs-mantenimiento-prensa-rep-query'),
    url(r'^rep/print/$','print_resumen_prensa', name='ogcs-mantenimiento-prensa-rep-print'),
)