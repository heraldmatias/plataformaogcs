# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('extras.views',   
    url(r'^mg/add/$','mgadd', name='ogcs-mantenimiento-mg-add'),
    url(r'^mg/consulta/$','mgquery', name='ogcs-mantenimiento-mg-query'),
    url(r'^mg/print/$','mgprint', name='ogcs-mantenimiento-mg-print'),
    url(r'^dig/add/$','digadd', name='ogcs-mantenimiento-dig-add'),
    url(r'^dig/consulta/$','digquery', name='ogcs-mantenimiento-dig-query'),
)
