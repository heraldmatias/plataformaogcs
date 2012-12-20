# -*- coding: utf-8 -*-

from django import forms
from models import Usuario
import django_tables2 as tables
from django_tables2.utils import A
from django.contrib.contenttypes.models import ContentType
import itertools

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        exclude = ('idusuario_mod','fec_mod','user','numero',
            'usuario','nivel','idusuario_creac','fec_creac')
        widgets = {
            'dependencia': forms.Select(),
            'organismo': forms.Select(attrs={'onChange':'dependencias(1);',}),
            'contrasena': forms.PasswordInput(),
            'usuario': forms.TextInput(attrs={'readonly':'readonly',}),
        }

class EditUsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        exclude = ('idusuario_mod','fec_mod','user','numero','usuario','nivel','contrasena')
        widgets = {
            'dependencia': forms.Select(),
            'organismo': forms.Select(attrs={'onChange':'dependencias(1);',}),
            'usuario': forms.TextInput(attrs={'readonly':'readonly',}),
        }

class ConsultaUsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ('organismo','dependencia','nombres','apellidos','estado')
        widgets = {
            'dependencia': forms.Select(),
            'organismo': forms.Select(attrs={'onChange':'dependencias(0);',}),
        }

class UsuarioTable(tables.Table):
    item = tables.Column()
    organismo = tables.Column(orderable=True)
    dependencia = tables.Column(orderable=True)
    nombres = tables.TemplateColumn('<a href={% url ogcs-mantenimiento-usuario-edit record.nivel_id record.numero %}>{{ record.nombres }}</a>',orderable=True)#tables.LinkColumn('ogcs-mantenimiento-usuario-edit', args=[1,A('numero')],orderable=True)
    apellidos = tables.Column(orderable=True) 
    sexo = tables.Column()
    usuario = tables.Column()
    email = tables.TemplateColumn('<a href={% url ogcs-mantenimiento-usuario-edit record.nivel_id record.numero %}>{{ record.email }}</a>',orderable=True)#tables.LinkColumn('ogcs-mantenimiento-usuario-edit', args=[1,A('numero')],orderable=True)
    estado = tables.Column(verbose_name='Estado')

    def render_item(self):
        value = getattr(self, '_counter', 1)
        self._counter = value + 1
        return '%d' % value

    class Meta:
        attrs = {"class": "table table-bordered table-condensed table-striped"}
        orderable = False

class AdministradorForm(forms.ModelForm):
    class Meta:
        model = Usuario
        exclude = ('idusuario_mod','fec_mod','user','numero','usuario','nivel')
        widgets = {
            'dependencia': forms.Select(),
            'organismo': forms.Select(attrs={'onChange':'dependencias(1);',}),
            'contrasena': forms.PasswordInput(),
            'usuario': forms.TextInput(attrs={'readonly':'readonly',}),
        }

class EditAdministradorForm(forms.ModelForm):
    class Meta:
        model = Usuario
        exclude = ('idusuario_mod','fec_mod','user','numero','usuario','nivel','contrasena')
        widgets = {
            'dependencia': forms.Select(),
            'organismo': forms.Select(attrs={'onChange':'dependencias(1);',}),
            'usuario': forms.TextInput(attrs={'readonly':'readonly',}),
        }

class ConsultaAdministradorForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ('organismo','dependencia','nombres','apellidos','estado')
        widgets = {
            'dependencia': forms.Select(),
            'organismo': forms.Select(attrs={'onChange':'dependencias(0);',}),
        }

class AdministradorTable(tables.Table):
    item = tables.Column()
    organismo = tables.Column(orderable=True)
    dependencia = tables.Column(orderable=True)
    nombres = tables.LinkColumn('ogcs-mantenimiento-admin-edit', args=[2,A('numero')],orderable=True)
    apellidos = tables.Column(orderable=True) 
    sexo = tables.Column()
    usuario = tables.Column()
    email = tables.LinkColumn('ogcs-mantenimiento-admin-edit', args=[2,A('numero')],orderable=True)
    estado = tables.Column(verbose_name='Estado')

    def render_item(self):
        value = getattr(self, '_counter', 1)
        self._counter = value + 1
        return '%d' % value

    class Meta:
        attrs = {"class": "table table-bordered table-condensed table-striped"}
        orderable = False

############################################################################
##################################AUDITORIA#################################
############################################################################
class AuditoriaConsultaForm(forms.Form):
    usuario = forms.ChoiceField(label='Usuario',
        choices=Usuario.objects.all().extra(select={
            'full_name':"concat(nombres,' ',apellidos)"}).order_by(
            'full_name').values_list('numero','full_name'))
    tabla = forms.ChoiceField(label='Tabla',
        choices=ContentType.objects.filter(
            id__in=[10,11,15,16,17,19,21,23,
            34,39,41,42,46,47,48,54,55,57]).extra(
            select={'name':'upper(name)'}).order_by(
            'name').values_list('id','name'))
    fechaini = forms.DateField(label='Fecha Desde',
        widget=forms.TextInput(attrs={'style':'width:100px;',}))
    fechafin = forms.DateField(label='Fecha Hasta',
        widget=forms.TextInput(attrs={'style':'width:100px;',}))
    titulo = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'style':'width:100%;'}), max_length=100)
    tipofecha = forms.ChoiceField(label="",choices=(
        (0,'Modificación'),(1,'Creación')),widget=forms.RadioSelect())

class AuditoriaTable(tables.Table):
    item = tables.Column(empty_values=())    
    descripcion = tables.Column(orderable=True)
    idusuario_creac = tables.Column(orderable=True,)#accessor='')
    fec_creac = tables.Column(orderable=True, verbose_name='Fecha de Creación')
    idusuario_mod = tables.Column(orderable=True, verbose_name='Usu Mod')
    fec_mod = tables.Column(orderable=True, verbose_name='Fecha Usu Mod')
    idadministrador_mod = tables.Column(orderable=True, verbose_name='Admin Mod')
    fec_modadm = tables.Column(orderable=True, verbose_name='Fecha Admin Mod')

    def __init__(self, *args, **kwargs):
        super(AuditoriaTable, self).__init__(*args, **kwargs)
        self.counter = itertools.count(1)

    def render_item(self):
        return '%d' % next(self.counter)

    class Meta:
        attrs = {"class": "table table-bordered table-condensed table-striped"}
        orderable = False