from django.contrib import admin
from models import Estado, Nivel, Organismo, Usuario

class ModelUsuario(admin.ModelAdmin):    
    list_display = ('codigo','numero','nombres','fono','email',)
    list_display_links = ('codigo','numero','nombres',)
    list_filter = ('nombres',)
    search_fields = ['^nombres',]
    list_per_page= 25
    list_max_show_all=50
    fieldsets = (
        ('Datos Personales', {
            'classes': ('collapse',),
            'description':'Rellene los campos con la informacion personal del Alumno',
            'fields': ('user','numero',('nombres',), ('sexo',),('nivel',),)
        }),
        ('Datos Adicionales', {
            'classes': ('collapse',),
	    'description':'Rellene la informacion adicional del alumno, algunos campos son opcionales', 	
            'fields': (('estado','organismo','dependencia',),('email','emailalt'), ('fono','anexo','celular',),)
        }),        
    )

admin.site.register(Usuario,ModelUsuario)
