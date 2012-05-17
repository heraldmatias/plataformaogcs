# -*- coding: utf-8 -*-
import django_tables2 as tables
from django_tables2.utils import A
from models import *
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
        fields = ('nombremmca', 'fechaini', 'fechafin', 'organismo', 'dependencia', )
        widgets = {
            'organismo': forms.Select(attrs={'onChange':'dependencias(0);', }),
            'dependencia':forms.Select(attrs={'disabled':'disabled', }),
            'fechaini': forms.TextInput(attrs={'size':'15', 'id':'id_fechaini_mcca'}),
            'fechafin': forms.TextInput(attrs={'size':'15', 'id':'id_fechafin_mcca'}),
        }
        exclude = ('idusuario_creac', 'idusuario_mod', )
        
class MccaForm_Estado(forms.ModelForm):
    class Meta:
        model = MccaEstado
        fields = ('organismo', 'dependencia')
        widgets = {
            'organismo': forms.Select(attrs={'onChange':'dependencias(0);', }),
            'dependencia':forms.Select(attrs={'disabled':'disabled', }),
        }

class MccaForm_EstadoTable(tables.Table):
    item = tables.Column()
    organismo = tables.TemplateColumn('<input type="hidden" name="corg" value="{{ record.organismo_id }}">{{ record.organismo }}')
    dependencia = tables.TemplateColumn('<input type="hidden" name="cdep" value="{{ record.dependencia }}">{{ record.nomdependecia }}')
    eliminar = tables.TemplateColumn('<a class="close" href="javascript: removedetalle(0,{{ record.item }})">×</a>')
    
    class Meta:
        attrs = {"class": "table table-bordered table-condensed table-striped", "id":"tabla_estado"}
        orderable = False


####################################################################################


class MccaForm_Privado(forms.ModelForm):
    class Meta:
        model = MccaPrivado
        fields = ('privado', )
      

class MccaForm_PrivadoTable(tables.Table):
    item = tables.Column()
    privado = tables.TemplateColumn('<input type="hidden" name="cpri" value="{{ record.privado }}">{{ record.privado }}')
    eliminar = tables.TemplateColumn('<a class="close" href="javascript: removedetalle(1,{{ record.item }})">×</a>')

    class Meta:
        attrs = {"class": "table table-bordered table-condensed table-striped", "id":"tabla_privado"}
        orderable = False
        
####################################################################################

class MccaForm_Indicador(forms.ModelForm):
    class Meta:
        model = MccaIndicador
        fields = ('indicador', )
       

class MccaForm_IndicadorTable(tables.Table):
    item = tables.Column()
    indicador = tables.TemplateColumn('<input type="hidden" name="cind" value="{{ record.indicador }}">{{ record.indicador }}')
    eliminar = tables.TemplateColumn('<a class="close" href="javascript: removedetalle(2,{{ record.item }})">×</a>')

    class Meta:
        attrs = {"class": "table table-bordered table-condensed table-striped", "id":"tabla_indicador"}
        orderable = False

####################################################################################

class MccaForm_Mensaje(forms.ModelForm):
    class Meta:
        model = MccaMensaje
        fields = ('mensaje', )


class MccaForm_MensajeTable(tables.Table):
    item = tables.Column()
    mensaje = tables.TemplateColumn('<input type="hidden" name="cmen" value="{{ record.mensaje }}">{{ record.mensaje }}')
    eliminar = tables.TemplateColumn('<a class="close" href="javascript: removedetalle(3,{{ record.item }})">×</a>')

    class Meta:
        attrs = {"class": "table table-bordered table-condensed table-striped", "id":"tabla_mensaje"}
        orderable = False

####################################################################################

class MccaForm_Canal(forms.ModelForm):
    class Meta:
        model = MccaCanal
        fields = ('tipommca', 'canal', )
        widgets = {
            'tipommca': forms.Select(),
        }
class MccaForm_CanalTable(tables.Table):
    item = tables.Column()
    canal = tables.TemplateColumn('<input type="hidden" name="ccan" value="{{ record.canal }}">{{ record.canal }}')
    tipommca = tables.TemplateColumn('<input type="hidden" name="ctipo" value="{{ record.tipommca_id }}">{{ record.tipommca }}')
    eliminar = tables.TemplateColumn('<a class="close" href="javascript: removedetalle(4,{{ record.item }})">×</a>')

    class Meta:
        attrs = {"class": "table table-bordered table-condensed table-striped", "id":"tabla_canal"}
        orderable = False

####################################################################################

class MccaForm_Accion(forms.ModelForm):
    class Meta:
        model = MccaAccion
        fields = ('acciones', 'fechainia', 'fechafina', )
        widgets = {
            'fechainia': forms.TextInput(attrs={'size':'15', 'id':'id_fechaini_acc', }),
            'fechafina': forms.TextInput(attrs={'size':'15', 'id':'id_fechafin_acc', }),
        }

class MccaForm_AccionTable(tables.Table):
    item = tables.Column()
    acciones = tables.TemplateColumn('<input type="hidden" name="cacc" value="{{ record.acciones }}">{{ record.acciones }}')
    fechainia = tables.TemplateColumn('<input type="hidden" name="caccfini" value="{{ record.fechainia }}">{{ record.fechainia }}')
    fechafina = tables.TemplateColumn('<input type="hidden" name="caccffin" value="{{ record.fechafina }}">{{ record.fechafina }}')
    eliminar = tables.TemplateColumn('<a class="close" href="javascript: removedetalle(5,{{ record.item }})">×</a>')

    class Meta:
        attrs = {"class": "table table-bordered table-condensed table-striped", "id":"tabla_accion"}
        orderable = False

####################################################################################

class MccaForm_Observacion(forms.ModelForm):
    class Meta:
        model = MccaObservacion
        fields = ('observacion', )

class MccaForm_ObservacionTable(tables.Table):
    item = tables.Column()
    observacion = tables.TemplateColumn('<input type="hidden" name="cobs" value="{{ record.observacion }}">{{ record.observacion }}')
    eliminar = tables.TemplateColumn('<a class="close" href="javascript: removedetalle(6,{{ record.item }})">×</a>')

    class Meta:
        attrs = {"class": "table table-bordered table-condensed table-striped", "id":"tabla_observacion"}
        orderable = False

####################################################################################
class ConsultaMccaForm(forms.ModelForm):
    class Meta:
        model = Mcca
        fields = ('organismo', 'dependencia', 'nombremmca', 'fechaini', 'fechafin')
        widgets = {
            'organismo': forms.Select(attrs={'onChange':'dependencias(0);', }),
            'dependencia':forms.Select(),
        }
        

class MccaTable(tables.Table):
    item = tables.Column()
    fechaini = tables.Column(orderable=True, verbose_name='Fecha')
    organismo = tables.Column(orderable=True, verbose_name='Organismo')
    dependencia = tables.Column(orderable=True, verbose_name='Dependecia')
    nombremmca = tables.Column(orderable=True, verbose_name='Nombre de Campaña')
    usuario = tables.Column(orderable=True, verbose_name='Usuario')
    fec_creac = tables.Column(orderable=True, verbose_name='Fecha de Creación')
    idusuario_mod = tables.Column(orderable=True, verbose_name='Usu Mod')
    fec_mod = tables.Column(orderable=True, verbose_name='Fecha Usu Mod')
    idadministrador_mod = tables.Column(orderable=True, verbose_name='Admin Mod')
    fec_modadm = tables.Column(orderable=True, verbose_name='Fecha Admin Mod')
    Modificar = tables.TemplateColumn('<a href=/comunicacion/mcca/edit/{{ record.nummcca }}/>modificar</a>')

    def render_item(self):
        value = getattr(self, '_counter', 1)
        self._counter = value + 1
        return '%d' % value

    class Meta:
        attrs = {"class": "table table-bordered table-condensed table-striped", "name":"tabla_consulta", "id":"tabla_consulta"}
        orderable = False
        
######################## MCCA FINAL ################################################
####################################################################################


######################## MCC INICIO ###############################################
####################################################################################

class MccForm(forms.ModelForm):
    class Meta:
        model = Mcc
        fields = ('nombremmc', 'nummcctipo', 'nummccestado', 'region', 'provincia', 'fechaini', 'fechafin', 'lugar', 'descripcionmcc', 'propuestamcc')
        widgets = {
            'nummcctipo': forms.Select(),
            'nummccestado': forms.Select(),
            'region': forms.Select(attrs={'onChange':'provincias(0);', }),
            #'provincia': forms.Select(attrs={'disabled':'disabled'}),
            'provincia': forms.Select(),
            'fechaini': forms.TextInput(attrs={'size':'15'}),
            'fechafin': forms.TextInput(attrs={'size':'15'}),
            'descripcionmcc': forms.Textarea(attrs={'class':'span20'}),
            'propuestamcc': forms.Textarea(attrs={'class':'span20'}),
        }
        exclude = ('idusuario_creac', 'idusuario_mod', )


class MccForm_Actor(forms.ModelForm):
    class Meta:
        model = MccActor
        fields = ('numtipovarios', 'actor', 'institucion', )
        widgets = {
            'numtipovarios': forms.Select(attrs={'id':'id_numtipovarios_ac'}),
            'institucion': forms.TextInput(attrs={'id':'id_institucion_ac'}),
        }
class MccForm_ActorTable(tables.Table):
    item = tables.Column()
    numtipovarios = tables.TemplateColumn('<input type="hidden" name="numtvac" value="{{ record.numtipovarios_id }}">{{ record.numtipovarios }}')
    actor = tables.TemplateColumn('<input type="hidden" name="listactor" value="{{ record.actor }}">{{ record.actor }}')
    institucion = tables.TemplateColumn('<input type="hidden" name="instac" value="{{ record.institucion }}">{{ record.institucion }}')
    eliminar = tables.TemplateColumn('<a class="close" href="javascript: removedetalle(0,{{ record.item }})">×</a>')

    class Meta:
        attrs = {"class": "table table-bordered table-condensed table-striped", "name":"tabla_actor", "id":"tabla_actor"}
        orderable = False

####################################################################################



class MccForm_Lider(forms.ModelForm):
    class Meta:
        model = MccLider
        fields = ('numtipovarios', 'lider', 'institucion', )
        widgets = {
            'numtipovarios': forms.Select(),
        }

class MccForm_LiderTable(tables.Table):
    item = tables.Column()
    numtipovarios = tables.TemplateColumn('<input type="hidden" name="numtvli" value="{{ record.numtipovarios_id }}">{{ record.numtipovarios }}')
    lider = tables.TemplateColumn('<input type="hidden" name="listlider" value="{{ record.lider }}">{{ record.lider }}')
    institucion = tables.TemplateColumn('<input type="hidden" name="instli" value="{{ record.institucion }}">{{ record.institucion }}')
    eliminar = tables.TemplateColumn('<a class="close" href="javascript: removedetalle(1,{{ record.item }})">×</a>')

    class Meta:
        attrs = {"class": "table table-bordered table-condensed table-striped", "name":"tabla_lider", "id":"tabla_lider"}
        orderable = False

####################################################################################

class MccForm_Observacion(forms.ModelForm):
    class Meta:
        model = MccObservacion
        fields = ('observacion', )
        

class MccForm_ObservacionTable(tables.Table):
    item = tables.Column()
    observacion = tables.TemplateColumn('<input type="hidden" name="cobs" value="{{ record.observacion }}">{{ record.observacion }}')
    eliminar = tables.TemplateColumn('<a class="close" href="javascript: removedetalle(2,{{ record.item }})">×</a>')

    class Meta:
        attrs = {"class": "table table-bordered table-condensed table-striped", "name":"tabla_observacion", "id":"tabla_observacion"}
        orderable = False

####################################################################################


class ConsultaMccForm(forms.ModelForm):
    class Meta:
        model = Mcc
        #fields = ('nombremmc','nummcctipo','nummccestado_id','region_id','provincia_id','fechaini','fechafin')
        fields = ('nombremmc', 'organismo', 'dependencia', 'nummcctipo', 'codigo', 'fechaini', 'fechafin', 'region', 'provincia', 'nummcctipo', 'nummccestado')
        widgets = {
            'nummcctipo': forms.Select(),
            'nummccestado': forms.Select(),
            'organismo': forms.Select(attrs={'onChange':'dependencias(0);', }),
            'dependencia':forms.Select(),
            'region': forms.Select(attrs={'onChange':'provincias(0);', }),
            'provincia':forms.Select(),
        }

class MccTable(tables.Table):
    item = tables.Column()
    fechaini = tables.Column(orderable=True, verbose_name='Fecha')
    organismo = tables.Column(orderable=True, verbose_name='Organismo')
    dependencia = tables.Column(orderable=True, verbose_name='Dependencia')
    nombremmc = tables.Column(orderable=True, verbose_name='Nombre de caso de crisis')
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
    Modificar = tables.TemplateColumn('<a href=/comunicacion/mcc/edit/{{ record.nummcc }}/>modificar</a>')
	
    def render_item(self):
        value = getattr(self, '_counter', 1)
        self._counter = value + 1
        return '%d' % value

    class Meta:
        attrs = {"class": "table table-bordered table-condensed table-striped"}
        orderable = False

######################## MCC FINAL ################################################
####################################################################################