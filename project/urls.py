# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    (r'^chat/', include('jqchat.urls')),
    (r'^grappelli/', include('grappelli.urls')),
    (r'^$', 'home.views.index'),
    (r'^home/', include('home.urls')),
    (r'^ubigeo/', include('ubigeo.urls')),
    (r'^dependencia/', include('dependencia.urls')),  
    (r'^usuario/', include('usuario.urls')),
    (r'^comunicacion/', include('comunicacion.urls')),
    (r'^extras/', include('extras.urls')),
	(r'^foro/', include('pybb.urls', namespace='pybb')),
    (r'^prensa/', include('prensa.urls')),
    (r'^calendar/', include('calendario.urls')),
)

from django.views.static import serve
urlpatterns += patterns('',
    url(r'^media/(?P<path>.*)$',
        serve, {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    url(r'^static/(?P<path>.*)$',
        serve, {'document_root': settings.STATIC_ROOT}),
    url(r'^favicon\.ico$', 
        'django.views.generic.simple.redirect_to', 
        {'url': '/static/images/favicon.ico'}),
)
handler500 = 'home.views.internal_error_view'
