# -*- coding: utf-8 -*-
from django import forms
from models import Evento
import django_tables2 as tables
import itertools

class EventoForm(forms.ModelForm):
	class Meta:
	    model = Evento
	    exclude = (
            'idusuario_creac',
            'fec_creac',
            'idusuario_mod',
            'fec_mod',
            'organismo',
            'dependencia',
            'fec_termin',
            'hor_termin')
	    widgets = {
            'titulo':forms.TextInput(attrs={'style':'width:100%;'}),
            'descripcion':forms.Textarea(attrs={'style':'width:100%;','rows':'4',}),
            'lugar':forms.TextInput(attrs={'style':'width:100%;'}),
            'fec_inicio' : forms.DateInput(attrs={"readonly":"readonly",'style':'width:80px;','title':'Fecha de Inicio'}),
            'hor_inicio' : forms.TextInput(attrs={"class":"vTimeField", 
                "readonly":"readonly",'style':'width:80px;','title':'Hora de Inicio'}),
            #'hor_termin' : forms.TextInput(attrs={"class":"vTimeField",
            #    "readonly":"readonly",'style':'width:80px;','title':'Hora de Termino'}),
            #'fec_termin' : forms.DateInput(attrs={"readonly":"readonly",'style':'width:80px;','title':'Fecha de Termino'}),            
            'url_edit' : forms.HiddenInput(),
            'region': forms.Select(attrs={'onChange':'get_provincias();',}),
            'provincia': forms.Select(attrs={'onChange':'get_distritos();',}),
        }

class EventoConsultaForm(forms.ModelForm):
    fechaini = forms.DateField(label='Fecha Desde',widget=forms.TextInput(attrs={'style':'width:100px;',}))
    #fechafin = forms.DateField(label='Fecha Hasta',widget=forms.TextInput(attrs={'style':'width:100px;',}))
    titulo = forms.CharField(required=True, widget=forms.TextInput(attrs={'style':'width:100%;'}), max_length=100)
    class Meta:
        model = Evento
        fields = ('organismo','dependencia','region','provincia','distrito')
        widgets = {
            'organismo': forms.Select(attrs={'onChange':'dependencias(0);',}),
            'dependencia':forms.Select(),
            'region': forms.Select(attrs={'onChange':'get_provincias();',}),
            'provincia': forms.Select(attrs={'onChange':'get_distritos();',}),
            'distrito': forms.Select(),
        }

class CalendarConsultaForm(forms.ModelForm):    
    class Meta:
        model = Evento
        fields = ('organismo','dependencia')
        widgets = {
            'organismo': forms.Select(attrs={'onChange':'dependencias(0);',}),
            'dependencia':forms.Select(),            
        }

class EventoTable(tables.Table):
    item = tables.TemplateColumn(""" <input type="hidden" 
        name="fila" id="id_fila" value="{{forloop.counter}}">{{forloop.counter}} """)
    titulo = tables.TemplateColumn(""" {{ record.titulo|truncatewords:8 }}  """,
    	verbose_name=u'Título',orderable=True)
    fec_inicio = tables.DateTimeColumn(format='d/m/Y',
    	verbose_name="Fecha Inicio",orderable=True)    
    #fec_termin = tables.DateTimeColumn(format='d/m/Y',
    #	verbose_name="Fecha Término",orderable=True)
    #hor_inicio = tables.TemplateColumn('{{record.hor_inicio}} - {{record.hor_termin}}',
    #	verbose_name="Duración",orderable=True)    
    acciones = tables.TemplateColumn("""
        {% if request.user.get_profile.organismo_id == record.organismo_id and request.user.get_profile.dependencia == record.dependencia %}
        <div style='text-align:center'>
    	<a href='{% url ogcs-mantenimiento-evento-edit record.codigo %}'>
    	<img src='{{ STATIC_URL }}images/icon_edit.png' width='15'
    	 height='15' alt='Modificar' title='Modificar' /></a>
        <a href='javascript:deleteEvent({{record.codigo}}, {{forloop.counter}})'>
        <img src='{{ STATIC_URL }}images/icon_trash.png' width='15' 
        height='15' alt='Eliminar' title='Eliminar' /></a></div>
        {% endif %}
        """, attrs={"td":{"width":"65px"}})

    class Meta:
        attrs = {"class": "table table-bordered table-condensed table-striped",'id':'tbl_eventos'}
        orderable = False