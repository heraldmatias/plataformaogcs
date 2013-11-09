# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url
#(?P<opcion>\w+)
urlpatterns = patterns('ubigeo.views',
    url(r'^region/add/$','regionadd', name='ogcs-mantenimiento-region-add'),
    url(r'^region/edit/(?P<codigo>\d+)/$','regionedit', name='ogcs-mantenimiento-region-edit'),
    url(r'^region/consulta/$','regionquery', name='ogcs-mantenimiento-region-consulta'),
    url(r'^region/imprimir/$','regionprint', name='ogcs-mantenimiento-region-print'),
    url(r'^provincia/imprimir/$','provinciaprint', name='ogcs-mantenimiento-provincia-print'),
    url(r'^provincia/add/$','provinciaadd', name='ogcs-mantenimiento-provincia-add'),
    url(r'^provincia/edit/(?P<region>\d+)/(?P<codigo>\d+)/$','provinciaedit', name='ogcs-mantenimiento-provincia-edit'),
    url(r'^provincia/consulta/$','provinciaquery', name='ogcs-mantenimiento-provincia-consulta'),
    url(r'^provincia/json/$','jsonprovincia', name='ogcs-provincia-jsonprovincia'),
    url(r'^distrito/json/$','jsondistrito', name='ogcs-distrito-jsondistrito'),
    url(r'^distrito/add/$', 'distritoadd', name='ogcs-mantenimiento-distrito-add'),
    url(r'^distrito/edit/(?P<region>\d+)/(?P<provincia>\d+)/(?P<codigo>\d+)/$','distritoedit', name='ogcs-mantenimiento-distrito-edit'),
    url(r'^distrito/consulta/$', 'distritoquery', name='ogcs-mantenimiento-distrito-consulta'),
)
