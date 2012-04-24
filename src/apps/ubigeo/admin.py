from django.contrib import admin
from models import Region, Provincia

class ModelRegion(admin.ModelAdmin):    
    list_display = ('codigo','numreg','region','estado','idusuario_creac','fec_creac','idusuario_mod','fec_mod',)
    list_display_links = ('codigo','numreg','region',)
    list_filter = ('codigo','region',)
    search_fields = ['^codigo','^region',]
    list_per_page= 20
    list_max_show_all=50
    fieldsets = (
        ('Datos de la Region', {
            'classes': ('collapse',),
            'description':'Rellene los datos con la informacion de la Region',
            'fields': (('numreg','region','estado',),)
        }),
    )

admin.site.register(Region,ModelRegion)
