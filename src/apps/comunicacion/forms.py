# -*- coding: utf-8 -*-
import django_tables2 as tables
from django_tables2.utils import A
from models import *
from django import forms
import itertools

class OacForm(forms.ModelForm):
    class Meta:
        model = Oac
        fields = ('archivo','estado')

class ConsultaOacForm(forms.ModelForm):
    class Meta:
        model = Oac
        fields = ('organismo','dependencia')
        widgets = {
            'organismo': forms.Select(attrs={'onChange':'dependencias(0);',}),
            'dependencia':forms.Select(),
        } 

class OacTable(tables.Table):
    item = tables.Column(empty_values=())
    organismo = tables.Column(orderable=True)
    dependencia = tables.Column(orderable=True)
    fec_creac = tables.Column(verbose_name='Fecha de Creación')
    idusuario_creac = tables.Column(verbose_name='Usuario')
    descargar = tables.TemplateColumn("""{% if record.estado_id == 1 %}
     <a href={{ record.urloac }}>Descargar</a>{% endif %}""",verbose_name="Descargar")
    #modificar = tables.TemplateColumn("""{% if record.idusuario_creac_id == user.get_profile.numero or user.is_superuser %}
    #    <a href={% url ogcs-mantenimiento-oac-edit record.codigo %}>Modificar</a>{% endif %}
    #    """,verbose_name="Modificar")

    def __init__(self, *args, **kwargs):
        super(OacTable, self).__init__(*args, **kwargs)
        self.counter = itertools.count(1)        
    
    def render_item(self):
        return '%d' % next(self.counter)

    class Meta:
        attrs = {"class": "table table-bordered table-condensed table-striped"}
        orderable = False

class PgcsForm(forms.ModelForm):
    class Meta:
        model = Pgcs
        fields = ('archivo',)

class PgcsAporteForm(forms.ModelForm):
    class Meta:
        model = Pgcs
        fields = ('organismo','dependencia','archivo',)
        widgets = {
            'organismo': forms.Select(attrs={'onChange':'dependencias(1);',}),
            'dependencia':forms.Select(),
        } 

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
    fec_creac = tables.Column(verbose_name='Fecha de Creación', orderable=True)
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
############################### LUGARES EN ACCION NUEVO ##########################################
class MccaForm_Lugar(forms.ModelForm):
    class Meta:
        model = MccaLugar
        fields = ('region', 'provincia','lugar')
        widgets = {
            'region': forms.Select(attrs={'onChange':'provincias(0);', }),
            'provincia': forms.Select(),
            'lugar': forms.TextInput(attrs={'style':'width:500px;'}),
        }

class MccaForm_LugarTable(tables.Table):
    item = tables.Column()
    region = tables.TemplateColumn('<input type="hidden" name="col_reg" value="{{ record.region_id }}">{{ record.region }}')
    provincia = tables.TemplateColumn('<input type="hidden" name="col_pro" value="{{ record.provincia_id }}">{{ record.provincia }}')
    lugar = tables.TemplateColumn('<input type="hidden" name="col_lug" value="{{ record.lugar }}">{{ record.lugar }}')
    eliminar = tables.TemplateColumn("{% if user.get_profile.nivel.codigo == 1 %}<a href='javascript: removedetalle(7,{{ record.item }})'><div id='delete'></div></a>{% endif %}")

    class Meta:
        attrs = {"class": "table table-bordered table-condensed table-striped", "name":"tabla_lugar", "id":"tabla_lugar"}
        orderable = False
############################### LUGARES EN ACCION NUEVO ##########################################
class MccaForm_Estado(forms.ModelForm):
    class Meta:
        model = MccaEstado
        fields = ('estado', )

class MccaForm_EstadoTable(tables.Table):
    item = tables.Column()
    estado = tables.TemplateColumn('<input type="hidden" name="cpest" value="{{ record.estado }}">{{ record.estado }}')
    eliminar = tables.TemplateColumn("{% if user.get_profile.nivel.codigo == 1 %}<a href='javascript: removedetalle(0,{{ record.item }})'><div id='delete'></div></a>{% endif %}")
    
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
    eliminar = tables.TemplateColumn("{% if user.get_profile.nivel.codigo == 1 %}<a href='javascript: removedetalle(1,{{ record.item }})'><div id='delete'></div></a>{% endif %}")

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
    eliminar = tables.TemplateColumn("{% if user.get_profile.nivel.codigo == 1 %}<a href='javascript: removedetalle(2,{{ record.item }})'><div id='delete'></div></a>{% endif %}")

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
    eliminar = tables.TemplateColumn("{% if user.get_profile.nivel.codigo == 1 %}<a href='javascript: removedetalle(3,{{ record.item }})'><div id='delete'></div></a>{% endif %}")

    class Meta:
        attrs = {"class": "table table-bordered table-condensed table-striped", "id":"tabla_mensaje"}
        orderable = False

####################################################################################

class MccaForm_Canal(forms.ModelForm):
    class Meta:
        model = MccaCanal
        fields = ('tipommca', 'canal', )
        widgets = {
            'tipommca': forms.Select(attrs={'style':'width:420px;',}),
            'canal': forms.TextInput(attrs={'style':'width:420px;',}),
        }
class MccaForm_CanalTable(tables.Table):
    item = tables.Column()
    canal = tables.TemplateColumn('<input type="hidden" name="ccan" value="{{ record.canal }}">{{ record.canal }}')
    tipommca = tables.TemplateColumn('<input type="hidden" name="ctipo" value="{{ record.tipommca_id }}">{{ record.tipommca }}')
    eliminar = tables.TemplateColumn("{% if user.get_profile.nivel.codigo == 1 %}<a href='javascript: removedetalle(4,{{ record.item }})'><div id='delete'></div></a>{% endif %}")

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
    fechainia = tables.TemplateColumn("""<input type="hidden" name="caccfini"
    value="{{ record.fechainia|date:"d/m/Y" }}">{{ record.fechainia|date:"d/m/Y" }}""")
    fechafina = tables.TemplateColumn("""<input type="hidden" name="caccffin"
     value="{{ record.fechafina|date:"d/m/Y" }}">{{ record.fechafina|date:"d/m/Y" }}""")
    eliminar = tables.TemplateColumn("{% if user.get_profile.nivel.codigo == 1 %}<a href='javascript: removedetalle(5,{{ record.item }})'><div id='delete'></div></a>{% endif %}")

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
    eliminar = tables.TemplateColumn("{% if user.get_profile.nivel.codigo == 1 %}<a href='javascript: removedetalle(6,{{ record.item }})'><div id='delete'></div></a>{% endif %}")

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
            'nombremmca': forms.TextInput(attrs={'style':'width:550px', }),
            'fechaini': forms.TextInput(attrs={'style':'width:100px;', }),
            'fechafin': forms.TextInput(attrs={'style':'width:100px;', }),
        }
        

class MccaTable(tables.Table):
    item = tables.Column(empty_values=())
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

    def __init__(self, *args, **kwargs):
        super(MccaTable, self).__init__(*args, **kwargs)
        self.counter = itertools.count(1)        
    
    def render_item(self):
        return '%d' % next(self.counter)

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
        fields = ('nombremmc', 'nummcctipo',  'fechaini', 'fechafin','descripcionmcc', 'mensajes', 'cuestionamientos')
        widgets = {
            'nummcctipo': forms.Select(),
            'fechaini': forms.TextInput(attrs={'size':'15'}),
            'fechafin': forms.TextInput(attrs={'size':'15'}),
            'descripcionmcc': forms.Textarea(attrs={'class':'span20','cols':'104'}),
            'mensajes': forms.Textarea(attrs={'class':'span20','cols':'104'}),
            'cuestionamientos': forms.Textarea(attrs={'class':'span20','cols':'104'}),
        }
        exclude = ('idusuario_creac', 'idusuario_mod', )

class MccForm_Lugar(forms.ModelForm):
    class Meta:
        model = MccLugar
        fields = ('region', 'provincia', 'distrito','lugar')
        widgets = {
            'region': forms.Select(attrs={'onChange':'get_provincias();', }),
            'provincia': forms.Select(attrs={'onChange':'get_distritos();', }),
            'distrito': forms.Select(),
            'lugar': forms.TextInput(attrs={'style':'width:500px;'}),
        }

class MccForm_LugarTable(tables.Table):
    item = tables.Column()
    region = tables.TemplateColumn('<input type="hidden" name="col_reg" value="{{ record.region_id }}">{{ record.region }}')
    provincia = tables.TemplateColumn('<input type="hidden" name="col_pro" value="{{ record.provincia_id }}">{{ record.provincia }}')
    distrito = tables.TemplateColumn('<input type="hidden" name="col_dis" value="{{ record.distrito_id }}">{{ record.distrito }}')
    lugar = tables.TemplateColumn('<input type="hidden" name="col_lug" value="{{ record.lugar }}">{{ record.lugar }}')
    eliminar = tables.TemplateColumn("{% if user.get_profile.nivel.codigo == 1 %}<a href='javascript: removedetalle(3,{{ record.item }})'><div id='delete'></div></a>{% endif %}")

    class Meta:
        attrs = {"class": "table table-bordered table-condensed table-striped", "name":"tabla_lugar", "id":"tabla_lugar"}
        orderable = False

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
    eliminar = tables.TemplateColumn("{% if user.get_profile.nivel.codigo == 1 %}<a href='javascript: removedetalle(0,{{ record.item }})'><div id='delete'></div></a>{% endif %}")

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
    eliminar = tables.TemplateColumn("{% if user.get_profile.nivel.codigo == 1 %}<a href='javascript: removedetalle(1,{{ record.item }})'><div id='delete'></div></a>{% endif %}")

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
    eliminar = tables.TemplateColumn("{% if user.get_profile.nivel.codigo == 1 %}<a href='javascript: removedetalle(2,{{ record.item }})'><div id='delete'></div></a>{% endif %}")

    class Meta:
        attrs = {"class": "table table-bordered table-condensed table-striped", "name":"tabla_observacion", "id":"tabla_observacion"}
        orderable = False

####################################################################################


class ConsultaMccForm(forms.ModelForm):
    class Meta:
        model = Mcc
        #fields = ('nombremmc','nummcctipo','nummccestado_id','region_id','provincia_id','fechaini','fechafin')
        fields = ('nombremmc', 'organismo', 'dependencia', 'nummcctipo', 'codigo', 'fechaini', 'fechafin', 'nummcctipo')
        widgets = {
            'nummcctipo': forms.Select(),
            'organismo': forms.Select(attrs={'onChange':'dependencias(0);', }),
            'dependencia':forms.Select(),
            #'region': forms.Select(attrs={'onChange':'provincias(0);', }),
            #'provincia':forms.Select(),
            'nombremmc': forms.TextInput(attrs={'style':'width:550px', }),
            'fechaini': forms.TextInput(attrs={'style':'width:100px;', }),
            'fechafin': forms.TextInput(attrs={'style':'width:100px;', }),
        }

class MccTable(tables.Table):
    item = tables.Column(empty_values=())
    fechaini = tables.Column(orderable=True, verbose_name='Fecha')
    organismo = tables.Column(orderable=True, verbose_name='Organismo')
    dependencia = tables.Column(orderable=True, verbose_name='Dependencia')
    nombremmc = tables.Column(orderable=True, verbose_name='Nombre de caso de crisis')
    nummcctipo = tables.Column(orderable=True, verbose_name='Tipo')
    nummccestado = tables.Column(orderable=True, verbose_name='Estado')    
    usuario = tables.Column(orderable=True, verbose_name='Usuario')
    fec_creac = tables.Column(orderable=True, verbose_name='Fecha de Creación')
    idusuario_mod = tables.Column(orderable=True, verbose_name='Usu Mod')
    fec_mod = tables.Column(orderable=True, verbose_name='Fecha Usu Mod')
    idadministrador_mod = tables.Column(orderable=True, verbose_name='Admin Mod')
    fec_modadm = tables.Column(orderable=True, verbose_name='Fecha Admin Mod')
    Modificar = tables.TemplateColumn('<a href=/comunicacion/mcc/edit/{{ record.nummcc }}/>modificar</a>')
	
    def __init__(self, *args, **kwargs):
        super(MccTable, self).__init__(*args, **kwargs)
        self.counter = itertools.count(1)        
    
    def render_item(self):
        return '%d' % next(self.counter)

    class Meta:
        attrs = {"class": "table table-bordered table-condensed table-striped"}
        orderable = False

######################## MCC FINAL ################################################
####################################################################################
