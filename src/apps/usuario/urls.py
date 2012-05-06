# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('usuario.views',
    url(r'^add/$','useradd', name='ogcs-mantenimiento-usuario-add'),
    url(r'^edit/(?P<codigo>\d+)/$','useredit', name='ogcs-mantenimiento-usuario-edit'),
    url(r'^consulta/$','userquery', name='ogcs-mantenimiento-usuario-query'),
    url(r'^imprimir/$','userprint', name='ogcs-mantenimiento-usuario-print'),
    url(r'^admin/add/$','adminadd', name='ogcs-mantenimiento-admin-add'),
    url(r'^admin/edit/(?P<codigo>\d+)/$','adminedit', name='ogcs-mantenimiento-admin-edit'),
    url(r'^admin/consulta/$','adminquery', name='ogcs-mantenimiento-admin-query'),
    url(r'^admin/imprimir/$','adminprint', name='ogcs-mantenimiento-admin-print'),
)
