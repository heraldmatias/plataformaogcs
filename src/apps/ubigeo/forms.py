# -*- coding: utf-8 -*-

from django import forms
from models import Region, Provincia
import django_tables2 as tables
from django_tables2.utils import A

REGIONES = list(Region.objects.all().values_list('numreg','region'))
REGIONES.append(('','TODOS'))

class RegionForm(forms.ModelForm):
    class Meta:
        model = Region
        exclude = ('numreg','idusuario_creac','idusuario_mod',)

class ConsultaRegionForm(forms.Form):
    region = forms.CharField(label="Digite el texto de busqueda:", required=False)

class ConsultaProvinciaForm(forms.Form):
    region = forms.ChoiceField(choices=REGIONES,label="Eliga la Región", required=False,initial='')
    provincia = forms.CharField(label="Digite el texto de busqueda",required=False)    

class RegionTable(tables.Table):
    item = tables.Column()
    region = tables.LinkColumn('ogcs-mantenimiento-region-edit', args=[A('numreg')],orderable=True)
    estado = tables.Column()    

    def render_item(self):
        value = getattr(self, '_counter', 1)
        self._counter = value + 1
        return '%d' % value

    class Meta:
        attrs = {"class": "table table-bordered table-condensed table-striped"}
        orderable = False

class ProvinciaTable(tables.Table):
    item = tables.Column()
    region = tables.Column(verbose_name="Región")
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
        #widgets = {
        #    'region': forms.Select(attrs={'class':'span2',}),
        #    'provincia': forms.TextInput(attrs={'class':'span8',}),
        #}
