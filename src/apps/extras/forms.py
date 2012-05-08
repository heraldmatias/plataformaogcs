# -*- coding: utf-8 -*-
import django_tables2 as tables
from django_tables2.utils import A
from models import MaterialGrafico
from django import forms

class MGForm(forms.ModelForm):
    class Meta:
        model = MaterialGrafico
        fields = ('arcmg1','arcmg2','arcmg3','arcmg4','arcmg5','arcmg6','arcmg7','arcmg8',)

class ConsultaMGForm(forms.ModelForm):
    class Meta:
        model = MaterialGrafico
        fields = ('organismo','dependencia')
        widgets = {
            'organismo': forms.Select(attrs={'onChange':'dependencias(0);',}),
            'dependencia':forms.Select(),
        } 

class MGTable(tables.Table):
    item = tables.Column()
    organismo = tables.Column(orderable=True)
    dependencia = tables.Column(orderable=True)
    fec_creac = tables.Column(verbose_name='Fecha de Creación')
    usuario = tables.Column(verbose_name='Usuario')
    Descargar = tables.TemplateColumn('<a href={{ record.urlmg1 }} target="_blank">Descargar</a>')
    Descargar = tables.TemplateColumn('<a href={{ record.urlmg2 }} target="_blank">Descargar</a>')
    Descargar = tables.TemplateColumn('<a href={{ record.urlmg3 }} target="_blank">Descargar</a>')
    Descargar = tables.TemplateColumn('<a href={{ record.urlmg4 }} target="_blank">Descargar</a>')
    Descargar = tables.TemplateColumn('<a href={{ record.urlmg5 }} target="_blank">Descargar</a>')
    Descargar = tables.TemplateColumn('<a href={{ record.urlmg6 }} target="_blank">Descargar</a>')
    Descargar = tables.TemplateColumn('<a href={{ record.urlmg7 }} target="_blank">Descargar</a>')
    Descargar = tables.TemplateColumn('<a href={{ record.urlmg8 }} target="_blank">Descargar</a>')

    def render_item(self):
        value = getattr(self, '_counter', 1)
        self._counter = value + 1
        return '%d' % value

    class Meta:
        attrs = {"class": "table table-bordered table-condensed table-striped"}
        orderable = False
