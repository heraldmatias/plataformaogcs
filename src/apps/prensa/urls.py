# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('prensa.views',   
    url(r'^rep/add/$','add_resumen_prensa', name='ogcs-mantenimiento-prensa-rep-add'),
    url(r'^rep/edit/(?P<codigo>\d+)/$','add_resumen_prensa', name='ogcs-mantenimiento-prensa-rep-edit'),
    url(r'^rep/consulta/$','query_resumen_prensa', name='ogcs-mantenimiento-prensa-rep-query'),
    url(r'^rep/print/$','print_resumen_prensa', name='ogcs-mantenimiento-prensa-rep-print'),
    url(r'^ce/add/$','add_caso_exito', name='ogcs-mantenimiento-prensa-ce-add'),
    url(r'^ce/edit/(?P<codigo>\d+)/$','add_caso_exito', name='ogcs-mantenimiento-prensa-ce-edit'),
    url(r'^ce/consulta/$','query_caso_exito', name='ogcs-mantenimiento-prensa-ce-query'),
    url(r'^ce/print/$','print_caso_exito', name='ogcs-mantenimiento-prensa-ce-print'),
)