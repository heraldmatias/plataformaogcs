# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('home.views',
    url(r'^$','main', name='ogcs-index'),
    url(r'^login/$','singin', name='ogcs-login'),    
    url(r'^logout/$','singout', name='ogcs-logout'),
)
