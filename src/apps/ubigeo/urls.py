# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url
#(?P<opcion>\w+)
urlpatterns = patterns('ubigeo.views',
    url(r'^region/add/$','regionadd', name='ogcs-mantenimiento-region-add'),
    url(r'^region/edit/(?P<codigo>\d+)/$','regionedit', name='ogcs-mantenimiento-region-edit'),
    url(r'^region/consulta/$','regionquery', name='ogcs-mantenimiento-region-consulta'),
    url(r'^provincia/add/$','provinciaadd', name='ogcs-mantenimiento-provincia-add'),
    url(r'^provincia/edit/(?P<codigo>\d+)/$','provinciaedit', name='ogcs-mantenimiento-provincia-edit'),
    url(r'^provincia/consulta/$','provinciaquery', name='ogcs-mantenimiento-provincia-consulta'),
    url(r'^provincia/json/$','jsonprovincia', name='ogcs-provincia-jsonprovincia'),
)
