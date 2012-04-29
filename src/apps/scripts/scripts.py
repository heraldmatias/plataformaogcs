from django.http import HttpResponse
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required

@login_required()
def imprimirToExcel(template,parametros,filename):
    html = render_to_string(template, parametros,)
    reporte = HttpResponse(content_type='application/ms-excel')
    reporte['Content-Disposition'] = 'attachment; filename='+filename
    reporte.write(html)    
    return reporte
