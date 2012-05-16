# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('comunicacion.views',
    url(r'^oac/add/$','oacadd', name='ogcs-mantenimiento-oac-add'),
    url(r'^oac/consulta/$','oacquery', name='ogcs-mantenimiento-oac-query'),
    url(r'^oac/print/$','oacprint', name='ogcs-mantenimiento-oac-print'),
    url(r'^pgcs/add/$','pgcsadd', name='ogcs-mantenimiento-pgcs-add'),
    url(r'^pgcs/consulta/$','pgcsquery', name='ogcs-mantenimiento-pgcs-query'),
    url(r'^pgcs/aporte/add/$','pgcs_apor_add', name='ogcs-mantenimiento-pgcs-aporte-add'),
    url(r'^pgcs/aporte/consulta/$','pgcs_apor_query', name='ogcs-mantenimiento-pgcs-aporte-query'),
    url(r'^pgcs/print/(?P<tipo>\d+)/$','pgcsprint', name='ogcs-mantenimiento-pgcs-print'),
	
	######################## MCCA ###############################################
	url(r'^mcca/add/$','mccaadd', name='ogcs-mantenimiento-mcca-add'),
	url(r'^mcca/consulta/$','mcca_query', name='ogcs-mantenimiento-mcca-query'),
	url(r'^mcca/print/$','mccaprint', name='ogcs-mantenimiento-mcca-print'),
	
	
	######################## MCC ################################################
	url(r'^mcc/add/$','mccadd', name='ogcs-mantenimiento-mcc-add'),
	url(r'^mcc/consulta/$','mcc_query', name='ogcs-mantenimiento-mcc-query'),
	url(r'^mcc/print/$','mccprint', name='ogcs-mantenimiento-mcc-print'),
)
