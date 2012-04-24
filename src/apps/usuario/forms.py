# -*- coding: utf-8 -*-

from django import forms
from models import Usuario
import django_tables2 as tables
from django_tables2.utils import A

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        exclude = ('idusuario_mod','fec_mod','user','numero')
        widgets = {
            'dependencia': forms.Select(),
            'organismo': forms.Select(attrs={'onChange':'dependencias();',}),
            'contrasena': forms.PasswordInput(),
        }

class ConsultaUsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ('organismo','dependencia','nivel','estado','nombres',)
        widgets = {
            'dependencia': forms.Select(),
            'organismo': forms.Select(attrs={'onChange':'dependencias();',}),
        }

class UsuarioTable(tables.Table):
    item = tables.Column()
    organismo = tables.Column()
    dependencia = tables.Column()
    nivel = tables.Column()
    nombres = tables.LinkColumn('ogcs-mantenimiento-usuario-edit', args=[A('numero')],orderable=True)
    sexo = tables.Column()
    email = tables.LinkColumn('ogcs-mantenimiento-usuario-edit', args=[A('numero')],orderable=True)
    estado = tables.Column(verbose_name='Estado')

    def render_item(self):
        value = getattr(self, '_counter', 1)
        self._counter = value + 1
        return '%d' % value

    class Meta:
        attrs = {"class": "table table-bordered table-condensed"}
        orderable = False
