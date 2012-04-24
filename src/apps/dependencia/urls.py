# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('dependencia.views',
    url(r'^ministerio/add/$','ministerioadd', name='ogcs-mantenimiento-ministerio-add'),
    url(r'^ministerio/edit/(?P<codigo>\d+)/$','ministerioedit', name='ogcs-mantenimiento-ministerio-edit'),
    url(r'^ministerio/consulta/$','ministerioquery', name='ogcs-mantenimiento-ministerio-consulta'),
    url(r'^odp/add/$','odpadd', name='ogcs-mantenimiento-odp-add'),
    url(r'^odp/edit/(?P<codigo>\d+)/$','odpedit', name='ogcs-mantenimiento-odp-edit'),
    url(r'^odp/consulta/$','odpquery', name='ogcs-mantenimiento-odp-consulta'),
    url(r'^gobernacion/add/$','gobernacionadd', name='ogcs-mantenimiento-gobernacion-add'),
    url(r'^gobernacion/edit/(?P<codigo>\d+)/$','gobernacionedit', name='ogcs-mantenimiento-gobernacion-edit'),
    url(r'^gobernacion/consulta/$','gobernacionquery', name='ogcs-mantenimiento-gobernacion-consulta'),
    url(r'^dependencias/json/$','jsondependencia', name='ogcs-dependencia-jsondependencia'),
)
