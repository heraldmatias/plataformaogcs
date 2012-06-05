# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('usuario.views',
    url(r'^add/(?P<nivel>\d+)/$','useradd', name='ogcs-mantenimiento-usuario-add'),
    url(r'^edit/(?P<nivel>\d+)/(?P<codigo>\d+)/$','useredit', name='ogcs-mantenimiento-usuario-edit'),
    url(r'^consulta/(?P<nivel>\d+)/$','userquery', name='ogcs-mantenimiento-usuario-consulta'),
    url(r'^imprimir/(?P<nivel>\d+)/$','userprint', name='ogcs-mantenimiento-usuario-print'),
    url(r'^auditoria/permisos/$','asignar_permisos', name='ogcs-mantenimiento-usuario-permisos'),
    url(r'^usuarios/json/$','jsonusuario', name='ogcs-usuario-jsonusuario'),
    #url(r'^admin/add/$','adminadd', name='ogcs-mantenimiento-admin-add'),
    #url(r'^admin/edit/(?P<codigo>\d+)/$','adminedit', name='ogcs-mantenimiento-admin-edit'),
    #url(r'^admin/consulta/$','adminquery', name='ogcs-mantenimiento-admin-query'),
    #url(r'^admin/imprimir/$','adminprint', name='ogcs-mantenimiento-admin-print'),
)
