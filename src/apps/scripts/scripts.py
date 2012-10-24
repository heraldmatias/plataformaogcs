#-*- coding: utf-8 -*-
from django.template.loader import render_to_string
from django.conf import settings
from django.http import HttpResponse
from django.template.context import Context
from django.template.loader import get_template
from xhtml2pdf import pisa # TODO: Change this when the lib changes.
import cStringIO as StringIO
import os
import cgi
from django.utils.safestring import mark_safe
from django.forms.util import ErrorList
class DivErrorList(ErrorList):
    def __unicode__(self):
        return self.as_divs()
    def as_divs(self):
        if not self: return u''
        return mark_safe('<div class="alert alert-error">%s</div>' % ''.join([u'<strong>%s</strong>' % e for e in self]))
#===============================================================================
# HELPERS
#===============================================================================
class UnsupportedMediaPathException(Exception):
    pass

def fetch_resources(uri, rel):
    """
Callback to allow xhtml2pdf/reportlab to retrieve Images,Stylesheets, etc.
`uri` is the href attribute from the html link element.
`rel` gives a relative path, but it's not used here.

"""
    if uri.startswith(settings.MEDIA_URL):
        path = os.path.join(settings.MEDIA_ROOT,
                            uri.replace(settings.MEDIA_URL, ""))
    elif uri.startswith(settings.STATIC_URL):
        path = os.path.join(settings.STATIC_ROOT,
                            uri.replace(settings.STATIC_URL, ""))
    else:
        raise UnsupportedMediaPathException(
                                'media urls must start with %s or %s' % (
                                settings.MEDIA_ROOT, settings.STATIC_ROOT))
    return path

def imprimirToPDF(html,filename):    
    reporte = None
    result = StringIO.StringIO()
    pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("UTF-8")), dest=result, link_callback=fetch_resources)
    #pdf = pisa.CreatePDF(html.encode("UTF-8"), result, encoding='UTF-8', link_callback=fetch_resources)
    if not pdf.err:
        reporte = HttpResponse(result.getvalue(), mimetype='application/pdf')
        reporte['Content-Disposition'] = 'attachment; filename='+filename
        return reporte 
    return HttpResponse('Error al generar el PDF: %s' % cgi.escape(html))

def imprimirToExcel(template,parametros,filename):
    html = render_to_string(template, parametros,)
    reporte = HttpResponse(content_type='application/ms-excel')
    reporte['Content-Disposition'] = 'attachment; filename='+filename
    reporte.write(html)    
    return reporte
