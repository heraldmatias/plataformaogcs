# -*- coding: utf-8 -*-

from django import forms
from models import Region, Provincia
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

