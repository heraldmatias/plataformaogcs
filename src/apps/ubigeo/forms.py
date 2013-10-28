# -*- coding: utf-8 -*-

from django import forms
from models import Region, Provincia, Distrito
import django_tables2 as tables
from django_tables2.utils import A

class RegionForm(forms.ModelForm):
    class Meta:
        model = Region
        exclude = ('numreg','idusuario_creac','idusuario_mod',)

class ConsultaRegionForm(forms.Form):
    region = forms.CharField(label="Digite el texto de busqueda:", required=False)

class ConsultaProvinciaForm(forms.ModelForm):
    provincia = forms.CharField(label="Digite el texto de busqueda",required=False)  
    class Meta:
        model = Provincia
        fields = ('region','provincia',)

class RegionTable(tables.Table):
    item = tables.Column()
    region = tables.LinkColumn('ogcs-mantenimiento-region-edit', args=[A('numreg')],orderable=True)
    estado = tables.Column()    

    def render_item(self):
        value = getattr(self, '_coo', 1)
        self._coo = value+1
        return '%d' % value

    class Meta:
        attrs = {"class": "table table-bordered table-condensed table-striped"}
        orderable = False

class ProvinciaTable(tables.Table):
    item = tables.Column()
    region = tables.Column(verbose_name="Región",orderable=True)
    provincia = tables.LinkColumn('ogcs-mantenimiento-provincia-edit', args=[A('numpro')],orderable=True)
    estado = tables.Column()    

    def render_item(self):
        value = getattr(self, '_counter', 1)
        self._counter = value + 1
        return '%d' % value

    class Meta:
        attrs = {"class": "table table-bordered table-condensed table-striped"}
        orderable = False

class ProvinciaForm(forms.ModelForm):
    class Meta:
        model = Provincia
        exclude = ('numpro','idusuario_creac','idusuario_mod',)


class DistritoForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(DistritoForm, self).__init__(*args, **kwargs)
        self.fields.keyOrder = ['region', 'provincia', 'distrito', 'estado']

    class Meta:
        model = Distrito
        exclude = ('numdis', 'idusuario_creac', 'idusuario_mod')
        widgets = {
            'region': forms.Select(attrs={'onChange':'get_provincias();',}),
        }

class ConsultaDistritoForm(forms.ModelForm):
    distrito = forms.CharField(label="Digite el texto de busqueda",required=False)
    class Meta:
        model = Distrito
        fields = ('region','provincia','distrito')
        widgets = {
            'region': forms.Select(attrs={'onChange':'get_provincias();',}),
        }

class DistritoTable(tables.Table):
    item = tables.Column()
    region = tables.Column(verbose_name="Región",orderable=True)
    provincia = tables.Column(verbose_name="Provincia",orderable=True)
    distrito = tables.LinkColumn('ogcs-mantenimiento-distrito-edit', args=[A('numdis')],orderable=True)
    estado = tables.Column()    

    def render_item(self):
        value = getattr(self, '_counter', 1)
        self._counter = value + 1
        return '%d' % value

    class Meta:
        attrs = {"class": "table table-bordered table-condensed table-striped"}
        orderable = False