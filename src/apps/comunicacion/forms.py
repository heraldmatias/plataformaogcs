# -*- coding: utf-8 -*-
import django_tables2 as tables
from django_tables2.utils import A
from models import Oac, Pgcs
from models import Mcc, MccObservacion, MccLider, MccActor
from models import MccEstado, Mcca, MccaEstado, MccaPrivado, MccaIndicador, MccaMensaje, MccaObservacion, MccaAccion, MccaCanal
from django import forms

class OacForm(forms.ModelForm):
    class Meta:
        model = Oac
        fields = ('archivo',)

class ConsultaOacForm(forms.ModelForm):
    class Meta:
        model = Oac
        fields = ('organismo','dependencia')
        widgets = {
            'organismo': forms.Select(attrs={'onChange':'dependencias(0);',}),
            'dependencia':forms.Select(),
        } 

class OacTable(tables.Table):
    item = tables.Column()
    organismo = tables.Column(orderable=True)
    dependencia = tables.Column(orderable=True)
    fec_creac = tables.Column(verbose_name='Fecha de Creación')
    usuario = tables.Column(verbose_name='Usuario')
    Descargar = tables.TemplateColumn('<a href={{ record.urloac }}>Descargar</a>')

    def render_item(self):
        value = getattr(self, '_counter', 1)
        self._counter = value + 1
        return '%d' % value

    class Meta:
        attrs = {"class": "table table-bordered table-condensed table-striped"}
        orderable = False

class PgcsForm(forms.ModelForm):
    class Meta:
        model = Pgcs
        fields = ('archivo',)

class ConsultaPgcsForm(forms.ModelForm):
    class Meta:
        model = Pgcs
        fields = ('organismo','dependencia')
        widgets = {
            'organismo': forms.Select(attrs={'onChange':'dependencias(0);',}),
            'dependencia':forms.Select(),
        } 

class PgcsTable(tables.Table):
    item = tables.Column()
    organismo = tables.Column(orderable=True)
    dependencia = tables.Column(orderable=True)
    fec_creac = tables.Column(verbose_name='Fecha de Creación')
    usuario = tables.Column(verbose_name='Usuario')
    Descargar = tables.TemplateColumn('<a href={{ record.urlpgcs }}>Descargar</a>')

    def render_item(self):
        value = getattr(self, '_counter', 1)
        self._counter = value + 1
        return '%d' % value

    class Meta:
        attrs = {"class": "table table-bordered table-condensed table-striped"}
        orderable = False

######################## MCCA INICIO ###############################################
####################################################################################

class MccaForm(forms.ModelForm):
    class Meta:
        model = Mcca
        fields = ('nombremmca', 'fechaini', 'fechafin', )
        widgets = {
            'fechaini': forms.TextInput(attrs={'size':'15'}),
            'fechafin': forms.TextInput(attrs={'size':'15'}),
        }
        
class MccaForm_Estado(forms.ModelForm):
    class Meta:
        model = MccaEstado
        fields = ('organismo', 'dependencia')
        widgets = {
            'organismo': forms.Select(attrs={'onChange':'dependencias(0);',}),
            'dependencia':forms.Select(attrs={'disabled':'disabled',}),
        }

class MccaForm_EstadoTable(tables.Table):
    item = tables.Column()
    organismo = tables.Column(orderable=True)
    dependencia = tables.Column(orderable=True)
    eliminar = tables.TemplateColumn('<a href="javascript:Eliminar_estado({{ record.item }})">Eliminar</a>')
    
    class Meta:
        attrs = {"class": "table table-bordered table-condensed table-striped", "name":"tabla_estado"}
        orderable = False


####################################################################################


class MccaForm_Privado(forms.ModelForm):
    class Meta:
        model = MccaPrivado
        fields = ('privado',)
      

class MccaForm_PrivadoTable(tables.Table):
    item = tables.Column()
    privado = tables.Column(orderable=True)
    eliminar = tables.TemplateColumn('<a href="javascript:Eliminar_privado({{ record.item }})">Eliminar</a>')

    class Meta:
        attrs = {"class": "table table-bordered table-condensed table-striped", "name":"tabla_privado"}
        orderable = False
        
####################################################################################

class MccaForm_Indicador(forms.ModelForm):
    class Meta:
        model = MccaIndicador
        fields = ('indicador',)
       

class MccaForm_IndicadorTable(tables.Table):
    item = tables.Column()
    indicador = tables.Column(orderable=True)
    eliminar = tables.TemplateColumn('<a href="javascript:Eliminar_indicador({{ record.item }})">Eliminar</a>')

    class Meta:
        attrs = {"class": "table table-bordered table-condensed table-striped", "name":"tabla_indicador"}
        orderable = False

####################################################################################

class MccaForm_Mensaje(forms.ModelForm):
    class Meta:
        model = MccaMensaje
        fields = ('mensaje',)


class MccaForm_MensajeTable(tables.Table):
    item = tables.Column()
    mensaje = tables.Column(orderable=True)
    eliminar = tables.TemplateColumn('<a href="javascript:Eliminar_mensaje({{ record.item }})">Eliminar</a>')

    class Meta:
        attrs = {"class": "table table-bordered table-condensed table-striped", "name":"tabla_mensaje"}
        orderable = False

####################################################################################

class MccaForm_Canal(forms.ModelForm):
    class Meta:
        model = MccaCanal
        fields = ('tipommca','canal',)
        widgets = {
            'tipommca': forms.Select(),
        }
class MccaForm_CanalTable(tables.Table):
    item = tables.Column()
    canal = tables.Column(orderable=True)
    tipommca_id = tables.Column(orderable=True)
    eliminar = tables.TemplateColumn('<a href="javascript:Eliminar_canal({{ record.item }})">Eliminar</a>')

    class Meta:
        attrs = {"class": "table table-bordered table-condensed table-striped", "name":"tabla_canal"}
        orderable = False

####################################################################################

class MccaForm_Accion(forms.ModelForm):
    class Meta:
        model = MccaAccion
        fields = ('acciones','fechaini','fechafin',)
        widgets = {
            'fechaini': forms.TextInput(attrs={'size':'15','id':'id_fechaini_acc',}),
            'fechafin': forms.TextInput(attrs={'size':'15','id':'id_fechafin_acc',}),
        }
class MccaForm_AccionTable(tables.Table):
    item = tables.Column()
    accion = tables.Column(orderable=True)
    fechaini = tables.Column(orderable=True)
    fechafin = tables.Column(orderable=True)
    eliminar = tables.TemplateColumn('<a href="javascript:Eliminar_accion({{ record.item }})">Eliminar</a>')

    class Meta:
        attrs = {"class": "table table-bordered table-condensed table-striped", "name":"tabla_accion"}
        orderable = False

####################################################################################

class MccaForm_Observacion(forms.ModelForm):
    class Meta:
        model = MccaObservacion
        fields = ('observacion',)

class MccaForm_ObservacionTable(tables.Table):
    item = tables.Column()
    observacion = tables.Column(orderable=True)
    eliminar = tables.TemplateColumn('<a href="javascript:Eliminar_observacion({{ record.item }})">Eliminar</a>')

    class Meta:
        attrs = {"class": "table table-bordered table-condensed table-striped", "name":"tabla_observacion"}
        orderable = False

####################################################################################
class ConsultaMccaForm(forms.ModelForm):
    class Meta:
        model = Mcca
        fields = ('organismo', 'dependencia', 'nombremmca', 'fechaini', 'fechafin')
        widgets = {
            'organismo': forms.Select(attrs={'onChange':'dependencias(0);',}),
            'dependencia':forms.Select(),
        }
    class Meta:
        model = MccaEstado
        fields = ('organismo', 'dependencia')
        widgets = {
            'organismo': forms.Select(attrs={'onChange':'dependencias(0);',}),
            'dependencia':forms.Select(),
        }

class MccaTable(tables.Table):
    item = tables.Column()
    fechaini = tables.Column(orderable=True, verbose_name='Fecha')
    organismo = tables.Column(orderable=True, verbose_name='Usuario')
    dependencia = tables.Column(orderable=True, verbose_name='Usuario')
    nombremmca = tables.Column(orderable=True, verbose_name='Nombre Campa&ntilde;a')
    usuario = tables.Column(orderable=True, verbose_name='Usuario')
    fec_creac = tables.Column(orderable=True, verbose_name='Fecha de Creación')
    idusuario_mod = tables.Column(orderable=True, verbose_name='Usu Mod')
    fec_mod = tables.Column(orderable=True, verbose_name='Fecha Usu Mod')
    idadministrador_mod = tables.Column(orderable=True, verbose_name='Admin Mod')
    fec_modadm = tables.Column(orderable=True, verbose_name='Fecha Admin Mod')
    Modificar = tables.TemplateColumn('<a href=/mcca/edit/>moidificar</a>')

    def render_item(self):
        value = getattr(self, '_counter', 1)
        self._counter = value + 1
        return '%d' % value

    class Meta:
        attrs = {"class": "table table-bordered table-condensed table-striped"}
        orderable = False
        
######################## MCCA FINAL ################################################
####################################################################################


######################## MCC INICIO ###############################################
####################################################################################

class MccForm(forms.ModelForm):
    class Meta:
        model = Mcc
        fields = ('nombremmc','nummcctipo','nummccestado','region','provincia', 'fechaini', 'fechafin','lugar','descripcionmcc','propuestamcc' )
        widgets = {
            'nummcctipo': forms.Select(),
            'nummccestado': forms.Select(),
            'region': forms.Select(),
            'provincia': forms.Select(attrs={'disabled':'disabled'}),
            'fechaini': forms.TextInput(attrs={'size':'15'}),
            'fechafin': forms.TextInput(attrs={'size':'15'}),
            'descripcionmcc': forms.Textarea(attrs={'class':'span20'}),
            'propuestamcc': forms.Textarea(attrs={'class':'span20'}),
        }

class MccForm_Actor(forms.ModelForm):
    class Meta:
        model = MccActor
        fields = ('numtipovarios','actor','institucion',)
        widgets = {
            'numtipovarios': forms.Select(attrs={'id':'id_numtipovarios_ac'}),
            'institucion': forms.TextInput(attrs={'id':'id_institucion_ac'}),
        }
class MccForm_ActorTable(tables.Table):
    item = tables.Column()
    numtipovarios = tables.Column(orderable=True)
    actor = tables.Column(orderable=True)
    institucion = tables.Column(orderable=True)
    eliminar = tables.TemplateColumn('<a href="javascript:Eliminar_actor({{ record.item }})">Eliminar</a>')

    class Meta:
        attrs = {"class": "table table-bordered table-condensed table-striped", "name":"tabla_canal"}
        orderable = False

####################################################################################



class MccForm_Lider(forms.ModelForm):
    class Meta:
        model = MccLider
        fields = ('numtipovarios','lider','institucion',)
        widgets = {
            'numtipovarios': forms.Select(),
        }

class MccForm_LiderTable(tables.Table):
    item = tables.Column()
    numtipovarios = tables.Column(orderable=True)
    lider = tables.Column(orderable=True)
    institucion = tables.Column(orderable=True)
    eliminar = tables.TemplateColumn('<a href="javascript:Eliminar_lider({{ record.item }})">Eliminar</a>')

    class Meta:
        attrs = {"class": "table table-bordered table-condensed table-striped", "name":"tabla_canal"}
        orderable = False

####################################################################################

class MccForm_Observacion(forms.ModelForm):
    class Meta:
        model = MccObservacion
        fields = ('observacion',)
        

class MccForm_ObservacionTable(tables.Table):
    item = tables.Column()
    observacion = tables.Column(orderable=True)
    eliminar = tables.TemplateColumn('<a href="javascript:Eliminar_observacion_mcc({{ record.item }})">Eliminar</a>')

    class Meta:
        attrs = {"class": "table table-bordered table-condensed table-striped", "name":"tabla_observacion"}
        orderable = False

####################################################################################


class ConsultaMccForm(forms.ModelForm):
    class Meta:
        model = Mcc
        #fields = ('nombremmc','nummcctipo','nummccestado_id','region_id','provincia_id','fechaini','fechafin')
        fields = ('nombremmc', 'nummcctipo', 'codigo', 'fechaini', 'fechafin', 'region', 'provincia')
        widgets = {
            #'organismo': forms.Select(attrs={'onChange':'dependencias(0);',}),
            #'dependencia':forms.Select(),
            'region': forms.Select(attrs={'onChange':'provincias(0);',}),
            'provincia':forms.Select(),
        }

class MccTable(tables.Table):
    item = tables.Column()
    fechaini = tables.Column(orderable=True, verbose_name='Fecha')
    #organismo = tables.Column(orderable=True,verbose_name='Organismo')
    #dependencia = tables.Column(orderable=True, verbose_name='Dependencia')
    nummcctipo = tables.Column(orderable=True, verbose_name='Tipo')
    nummccestado = tables.Column(orderable=True, verbose_name='Estado')
    region = tables.Column(orderable=True, verbose_name='Región')
    provincia = tables.Column(orderable=True, verbose_name='Provincia')
    usuario = tables.Column(orderable=True, verbose_name='Usuario')
    fec_creac = tables.Column(orderable=True, verbose_name='Fecha de Creación')
    idusuario_mod = tables.Column(orderable=True, verbose_name='Usu Mod')
    fec_mod = tables.Column(orderable=True, verbose_name='Fecha Usu Mod')
    idadministrador_mod = tables.Column(orderable=True, verbose_name='Admin Mod')
    fec_modadm = tables.Column(orderable=True, verbose_name='Fecha Admin Mod')
    Modificar = tables.TemplateColumn('<a href=/mcca/edit/>moidificar</a>')

    def render_item(self):
        value = getattr(self, '_counter', 1)
        self._counter = value + 1
        return '%d' % value

    class Meta:
        attrs = {"class": "table table-bordered table-condensed table-striped"}
        orderable = False

######################## MCC FINAL ################################################
####################################################################################
