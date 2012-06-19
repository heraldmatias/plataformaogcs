# -*- coding: utf-8 -*-
import django_tables2 as tables
from django_tables2.utils import A
from models import MaterialGrafico, DocumentoInteresGeneral, ActaReunionIntersectorial, Documento, CATEGORIAS
from usuario.models import Organismo, Usuario
from pybb.models import Category, Forum
from django import forms
from django.utils.safestring import mark_safe
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
    Descargar = tables.TemplateColumn('<a href={% url ogcs-descarga record.Descargar %}>Descargar</a>')
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
    Descargar = tables.TemplateColumn('<a href={% url ogcs-descarga record.Descargar %}>Descargar</a>')
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
        widgets = {
            'nombreari': forms.TextInput(attrs={'style':'width:470px', }),
        } 

class ConsultaAriForm(forms.ModelForm):
    class Meta:
        model = ActaReunionIntersectorial
        fields = ('nombreari',)
        widgets = {
            'nombreari': forms.TextInput(attrs={'style':'width:350px', }),
        }
        #widgets = {
        #    'organismo': forms.Select(attrs={'onChange':'dependencias(0);',}),
        #    'dependencia':forms.Select(),
        #} 

class AriTable(tables.Table):
    item = tables.Column()
    organismo = tables.Column(orderable=True)
    dependencia = tables.Column(orderable=True)
    nombreari = tables.Column(verbose_name='Reunión',orderable=True)
    fec_creac = tables.Column(verbose_name='Fecha de Creación')
    usuario = tables.Column(verbose_name='Usuario',)
    Descargar = tables.TemplateColumn('<a href={% url ogcs-descarga record.archari.name %}>Descargar</a>')

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
    idusuario_creac = tables.Column(verbose_name='Usuario',accessor='idusuario_creac.usuario',orderable=True)
    Descargar = tables.TemplateColumn('<a href={% url ogcs-descarga record.archivo.name %}>Descargar</a>')

    def render_item(self):
        value = getattr(self, '_counter', 1)
        self._counter = value + 1
        return '%d' % value

    class Meta:
        attrs = {"class": "table table-bordered table-condensed table-striped"}
        orderable = False

########################################################
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name','position','hidden')
        widgets = {
            'name': forms.TextInput(attrs={'style':'width:560px;'}),
            'position': forms.TextInput(attrs={'style':'width:30px;'}),
        }

class CategoryConsultaForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name',)
        widgets = {
            'name': forms.TextInput(attrs={'style':'width:500px;'}),            
        }

class CategoryTable(tables.Table):
    item = tables.Column()
    Categoria = tables.TemplateColumn('<a href={% url ogcs-mantenimiento-categoria-edit record.id %}>{{ record.name }}</a>',orderable=True)
    Posicion = tables.TemplateColumn('{{ record.position }}',orderable=True)    
    hidden = tables.Column(orderable=True)    
    def render_item(self):
        value = getattr(self, '_counter', 1)
        self._counter = value + 1
        return '%d' % value

    class Meta:
        attrs = {"class": "table table-bordered table-condensed table-striped"}
        orderable = False

class ForumForm(forms.ModelForm):    
    class Meta:
        model = Forum
        fields = ('name','position','hidden')
        widgets = {
            'name': forms.TextInput(attrs={'id':'id_name_foro','name':'name_foro','style':'width:560px;'}),
            'position': forms.TextInput(attrs={'id':'id_position_foro','style':'width:30px;'}),
            'hidden': forms.CheckboxInput(attrs={'id':'id_hidden_foro'}),
        }
class ForumTable(tables.Table):
    item = tables.Column()
    name = tables.TemplateColumn('<input type="hidden" name="cforo" value="{{ record.name }}">{{ record.name }}',orderable=True,verbose_name='Foro')
    position = tables.TemplateColumn('<input type="hidden" name="cpos" value="{{ record.position }}">{{ record.position }}',verbose_name='Posicion',orderable=True)    
    admins = tables.TemplateColumn('<input type="hidden" name="chid" value="{{ record.hidden }}">{% if record.hidden %} SI{% else %}NO{% endif %}',verbose_name='Solo Administrador',orderable=True)
    #post_count = tables.Column(verbose_name='Numero Posts',orderable=True)
    #topic_count = tables.Column(verbose_name='Numero Temas',orderable=True)
    eliminar = tables.Column()
    def render_item(self):
        value = getattr(self, '_counter', 1)
        self._counter = value + 1
        return '%d' % value

    def render_eliminar(self):
        value = getattr(self, '_counterr', 1)  
        self._counterr = value + 1      
        return mark_safe('<a href="javascript: removedetalle(%d)"><div id="delete"></div></a>' % value)

    class Meta:
        attrs = {"class": "table table-bordered table-condensed table-striped",'id':'id_foros'}
        orderable = False
