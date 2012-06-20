# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('extras.views',   
    url(r'^mg/add/$','mgadd', name='ogcs-mantenimiento-mg-add'),
    url(r'^mg/consulta/$','mgquery', name='ogcs-mantenimiento-mg-query'),
    url(r'^mg/print/$','mgprint', name='ogcs-mantenimiento-mg-print'),
    url(r'^dig/add/$','digadd', name='ogcs-mantenimiento-dig-add'),
    url(r'^dig/consulta/$','digquery', name='ogcs-mantenimiento-dig-query'),
    url(r'^dig/print/$','digprint', name='ogcs-mantenimiento-dig-print'),
    url(r'^ari/add/$','ariadd', name='ogcs-mantenimiento-ari-add'),
    url(r'^ari/consulta/$','ariquery', name='ogcs-mantenimiento-ari-query'),
    url(r'^ari/print/$','ariprint', name='ogcs-mantenimiento-ari-print'),
    url(r'^documentos/add/$','documentos_add', name='ogcs-mantenimiento-doc-add'),
    url(r'^documentos/consulta/$','documentos_query', name='ogcs-mantenimiento-doc-query'),
    url(r'^documentos/print/$','documentos_print', name='ogcs-mantenimiento-doc-print'),
    url(r'^descarga/(?P<archivoo>[a-zA-Z0-9_./]+)/$','descargar', name='ogcs-descarga'), 
    url(r'^categoria/add/$','categoria_add', name='ogcs-mantenimiento-categoria-add'),
    url(r'^categoria/edit/(?P<codigo>\d+)/$','categoria_edit', name='ogcs-mantenimiento-categoria-edit'),
    url(r'^categoria/consulta/$','categoria_query', name='ogcs-mantenimiento-categoria-query'),   
    url(r'^forum/add/$','forum_add', name='ogcs-mantenimiento-foro-add'),
    url(r'^forum/edit/(?P<codigo>\d+)/$','forum_edit', name='ogcs-mantenimiento-foro-edit'),
    url(r'^forum/consulta/$','forum_query', name='ogcs-mantenimiento-foro-query'),

)
