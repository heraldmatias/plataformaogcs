# -*- coding: utf-8 -*-
import django_tables2 as tables
from django_tables2.utils import A
from models import MaterialGrafico, DocumentoInteresGeneral, ActaReunionIntersectorial, Documento, CATEGORIAS
from usuario.models import Organismo, Usuario
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
    Descargar = tables.TemplateColumn('<a href={{ record.Descargar }} target="_blank">Descargar</a>')
    Tipo = tables.Column(orderable=True)
    def render_item(self):
        value = getattr(self, '_counter', 1)
        self._counter = value + 1
        return '%d' % value

    class Meta:
        attrs = {"class": "table table-bordered table-condensed table-striped"}
        orderable = False

class DIGForm(forms.ModelForm):
    class Meta:
        model = DocumentoInteresGeneral
        fields = ('archmis1','archmis2','archmis3','archaca1','archaca2','archaca3','archbue1','archbue2','archbue3',)

class ConsultaDIGForm(forms.ModelForm):
    class Meta:
        model = DocumentoInteresGeneral
        fields = ('organismo','dependencia')
        widgets = {
            'organismo': forms.Select(attrs={'onChange':'dependencias(0);',}),
            'dependencia':forms.Select(),
        } 

class DIGTable(tables.Table):
    item = tables.Column()
    organismo = tables.Column(orderable=True)
    dependencia = tables.Column(orderable=True)
    fec_creac = tables.Column(verbose_name='Fecha de Creación')
    usuario = tables.Column(verbose_name='Usuario')
    Descargar = tables.TemplateColumn('<a href={{ record.Descargar }} target="_blank">Descargar</a>')
    TipoArchivo = tables.Column(orderable=True)
    Tipo = tables.Column(orderable=True)
    def render_item(self):
        value = getattr(self, '_counter', 1)
        self._counter = value + 1
        return '%d' % value

    class Meta:
        attrs = {"class": "table table-bordered table-condensed table-striped"}
        orderable = False

class AriForm(forms.ModelForm):
    class Meta:
        model = ActaReunionIntersectorial
        fields = ('archari','nombreari')

class ConsultaAriForm(forms.ModelForm):
    class Meta:
        model = ActaReunionIntersectorial
        fields = ('organismo','dependencia','nombreari')
        widgets = {
            'organismo': forms.Select(attrs={'onChange':'dependencias(0);',}),
            'dependencia':forms.Select(),
        } 

class AriTable(tables.Table):
    item = tables.Column()
    organismo = tables.Column(orderable=True)
    dependencia = tables.Column(orderable=True)
    nombreari = tables.Column(verbose_name='Reunión',orderable=True)
    fec_creac = tables.Column(verbose_name='Fecha de Creación')
    usuario = tables.Column(verbose_name='Usuario',)
    Descargar = tables.TemplateColumn('<a href={{ record.urlari }}>Descargar</a>')

    def render_item(self):
        value = getattr(self, '_counter', 1)
        self._counter = value + 1
        return '%d' % value

    class Meta:
        attrs = {"class": "table table-bordered table-condensed table-striped"}
        orderable = False

class DocumentoForm(forms.ModelForm):
    class Meta:
        model = Documento
        fields = ('archivo',)        

class ConsultaDocumentoForm(forms.ModelForm):    
    class Meta:
        model = Documento
        fields = ('idusuario_creac','organismo','dependencia','categoria','tipo') 
        widgets = {
            'organismo': forms.Select(attrs={'onchange':'dependencias(0);'}),
            'dependencia': forms.Select(),
            'idusuario_creac': forms.Select(),
            'tipo': forms.Select(),
        }

class DocumentoTable(tables.Table):
    item = tables.Column()
    organismo = tables.Column(orderable=True)
    dependencia = tables.Column(orderable=True)    
    tipo = tables.Column(orderable=True)
    categoria = tables.Column(orderable=True)        
    fec_creac = tables.Column(verbose_name='Fecha de Creación',orderable=True)
    usuario = tables.Column(verbose_name='Usuario',orderable=True)
    Descargar = tables.TemplateColumn('<a href={{ record.url_archivo }}>Descargar</a>')

    def render_item(self):
        value = getattr(self, '_counter', 1)
        self._counter = value + 1
        return '%d' % value

    class Meta:
        attrs = {"class": "table table-bordered table-condensed table-striped"}
        orderable = False

