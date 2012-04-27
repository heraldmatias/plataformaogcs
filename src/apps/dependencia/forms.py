# -*- coding: utf-8 -*-

from django import forms
from models import Ministerio, Odp, Gobernacion
from ubigeo.models import Region, Provincia
import django_tables2 as tables
from django_tables2.utils import A
from ubigeo.forms import REGIONES
from ubigeo.models import Provincia

PROVINCIAS = list(Provincia.objects.all().values_list('numpro','provincia'))
PROVINCIAS.append(('','TODOS'))

MINISTERIOS = list(Ministerio.objects.all().values_list('nummin','ministerio'))
MINISTERIOS.append(('','TODOS'))

class MinisterioForm(forms.ModelForm):
    class Meta:
        model = Ministerio
        fields = ('ministerio','iniciales','estado')

class ConsultaMinisterioForm(forms.Form):
    ministerio = forms.CharField(label="Digite el texto de busqueda:", required=False)

class MinisterioTable(tables.Table):
    item = tables.Column()
    ministerio = tables.LinkColumn('ogcs-mantenimiento-ministerio-edit', args=[A('nummin')],orderable=True)
    estado = tables.Column()    

    def render_item(self):
        value = getattr(self, '_counter', 1)
        self._counter = value + 1
        return '%d' % value

    class Meta:
        attrs = {"class": "table table-bordered table-condensed"}
        orderable = False


class OdpForm(forms.ModelForm):
    class Meta:
        model = Odp
        fields = ('nummin','odp','iniciales','estado')

class ConsultaOdpForm(forms.Form):#CORREGIR
    nummin = forms.ChoiceField(choices=MINISTERIOS,label='Ministerio',required=False,initial='')
    odp = forms.CharField(label='Nombre de Odp', max_length=70,required=False)

class OdpTable(tables.Table):
    item = tables.Column()
    nummin = tables.Column()
    odp = tables.LinkColumn('ogcs-mantenimiento-odp-edit', args=[A('numodp')],orderable=True,)
    iniciales = tables.Column()
    estado = tables.Column()    

    def render_item(self):
        value = getattr(self, '_counter', 1)
        self._counter = value + 1
        return '%d' % value

    class Meta:
        attrs = {"class": "table table-bordered table-condensed"}
        orderable = False

class GobernacionForm(forms.ModelForm):
    region= forms.ChoiceField(choices=REGIONES,widget=forms.Select(attrs={'onChange':'provincias();',}))
    class Meta:
        model = Gobernacion
        fields = ('provincia','gobernacion','iniciales','estado')
        widgets = {
            'region': forms.Select(attrs={'onChange':'provincias();',}),
        }

class ConsultaGobernacionForm(forms.Form):
    region = forms.ChoiceField(choices=REGIONES,label='Region',required=False,widget=forms.Select(attrs={'onChange':'provincias();',}))
    provincia = forms.ChoiceField(choices=PROVINCIAS,label='Provincia',required=False)
    

class GobernacionTable(tables.Table):
    item = tables.Column()
    region = tables.Column()
    provincia = tables.Column()
    gobernacion = tables.LinkColumn('ogcs-mantenimiento-gobernacion-edit', args=[A('numgob')],orderable=True)
    iniciales = tables.Column()
    estado = tables.Column()    

    def render_item(self):
        value = getattr(self, '_counter', 1)
        self._counter = value + 1
        return '%d' % value

    class Meta:
        attrs = {"class": "table table-bordered table-condensed"}
        orderable = False
