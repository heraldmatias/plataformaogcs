# -*- coding: utf-8 -*-

from django import forms
from models import Usuario
import django_tables2 as tables
from django_tables2.utils import A

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        exclude = ('idusuario_mod','fec_mod','user','numero','usuario','nivel')
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
