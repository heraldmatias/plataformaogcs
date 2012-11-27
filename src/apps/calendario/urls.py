# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('calendario.views',
    url(r'^evento/add/$','eventoadd', name='ogcs-mantenimiento-evento-add'),
    url(r'^evento/edit/(?P<codigo>\d+)/$','eventoadd', name='ogcs-mantenimiento-evento-edit'),
    url(r'^evento/consulta/$','eventoquery', name='ogcs-mantenimiento-evento-query'),
    url(r'^evento/delete/$','eventodelete', name='ogcs-mantenimiento-evento-delete'),
    #url(r'^evento/print/$','eventoprint', name='ogcs-mantenimiento-evento-print'),
)