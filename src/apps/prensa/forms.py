# -*- coding: utf-8 -*-
from models import ResumenPrensa, CasoExito
from django import forms
import django_tables2 as tables
import itertools

class ResumenPrensaForm(forms.ModelForm):
    class Meta:
        model = ResumenPrensa
        fields = ('descripcion','archivo','estado','fecha')
        widgets = {
            'descripcion': forms.Textarea(attrs={'style':'width:90%','rows':'6'}),            
        }

class ConsultaRepForm(forms.ModelForm):
    fechaini = forms.DateField(label='Fecha Desde',widget=forms.TextInput(attrs={'style':'width:100px;',}))
    fechafin = forms.DateField(label='Fecha Hasta',widget=forms.TextInput(attrs={'style':'width:100px;',}))
    class Meta:
        model = ResumenPrensa
        fields = ('organismo','dependencia')
        widgets = {
            'organismo': forms.Select(attrs={'onChange':'dependencias(0);',}),
            'dependencia':forms.Select(),            
        }

class RepTable(tables.Table):
    item = tables.Column(empty_values=())
    organismo = tables.Column(orderable=True)
    dependencia = tables.Column(orderable=True)
    fecha = tables.DateColumn(format="d/m/Y",verbose_name='Fecha',orderable=True)
    descripcion = tables.TemplateColumn("{{ record.descripcion|truncatewords:10 }}")    
    fec_creac = tables.DateColumn(format="d/m/Y H:i a",verbose_name='Fecha de Registro',orderable=True)
    idusuario_creac = tables.Column(verbose_name='Usuario',)
    descargar = tables.TemplateColumn('<a href={% url ogcs-descarga record.archivo %}>Descargar</a>',verbose_name="Descargar")
    modificar = tables.TemplateColumn("""{% if record.idusuario_creac_id == user.get_profile.numero %}
        <a href={% url ogcs-mantenimiento-prensa-rep-edit record.codigo %}>Modificar</a>{% endif %}
        """,verbose_name="Modificar")
    def __init__(self, *args, **kwargs):
        super(RepTable, self).__init__(*args, **kwargs)
        self.counter = itertools.count(1)        
    
    def render_item(self):
        return '%d' % next(self.counter)

    class Meta:
        attrs = {"class": "table table-bordered table-condensed table-striped"}
        orderable = False

class CasoExitoForm(forms.ModelForm):
    class Meta:
        model = CasoExito
        fields = ('descripcion','archivo','estado','fecha')
        widgets = {
            'descripcion': forms.Textarea(attrs={'style':'width:90%','rows':'6'}),
        }

class ConsultaCeForm(forms.ModelForm):
    fechaini = forms.DateField(label='Fecha de registro',widget=forms.TextInput(attrs={'style':'width:100px;',}))
    #fechafin = forms.DateField(label='Fecha Hasta',widget=forms.TextInput(attrs={'style':'width:100px;',}))
    class Meta:
        model = CasoExito
        fields = ('organismo','dependencia')
        widgets = {
            'organismo': forms.Select(attrs={'onChange':'dependencias(0);',}),
            'dependencia':forms.Select(),            
        }

class CeTable(tables.Table):
    item = tables.Column(empty_values=())
    organismo = tables.Column(orderable=True)
    dependencia = tables.Column(orderable=True)
    fecha = tables.DateColumn(format="d/m/Y",verbose_name='Fecha de Registro',orderable=True)
    descripcion = tables.TemplateColumn("{{ record.descripcion|truncatewords:10 }}")    
    fec_creac = tables.DateColumn(format="d/m/Y H:i a",verbose_name='Fecha de creación',orderable=True)
    idusuario_creac = tables.Column(verbose_name='Usuario',)
    descargar = tables.TemplateColumn('<a href={% url ogcs-descarga record.archivo %}>Descargar</a>',verbose_name="Descargar")
    #modificar = tables.TemplateColumn("""{% if record.idusuario_creac_id == user.get_profile.numero %}
    #    <a href={% url ogcs-mantenimiento-prensa-ce-edit record.codigo %}>Modificar</a>{% endif %}
    #    """,verbose_name="Modificar")
    def __init__(self, *args, **kwargs):
        super(CeTable, self).__init__(*args, **kwargs)
        self.counter = itertools.count(1)        
    
    def render_item(self):
        return '%d' % next(self.counter)

    class Meta:
        attrs = {"class": "table table-bordered table-condensed table-striped"}
        orderable = False
