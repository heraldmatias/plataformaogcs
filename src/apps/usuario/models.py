# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User

SEXO = (
        ('FE','FEMENINO'),
        ('MA','MASCULINO'),
        )

class Estado(models.Model):
    codigo = models.AutoField(verbose_name='Codigo', primary_key=True)
    nombre = models.CharField(verbose_name='Nombre', unique=True, max_length=45)
    class Meta:
        db_table = u'estado'
        verbose_name = u'Estado'
        verbose_name_plural = u'Estados'

    def __unicode__(self):
        return self.nombre

class Nivel(models.Model):
    codigo = models.AutoField(verbose_name='Codigo', primary_key=True)
    nombre = models.CharField(verbose_name='Nombre', unique=True, max_length=45)
    class Meta:
        db_table = u'nivel'
        verbose_name = u'Nivel'
        verbose_name_plural = u'Niveles'

    def __unicode__(self):
        return self.nombre

class Organismo(models.Model):
    codigo = models.AutoField(verbose_name='Codigo', primary_key=True)
    nombre = models.CharField(verbose_name='Nombre', unique=True, max_length=105)
    class Meta:
        db_table = u'organismo'
        verbose_name = u'Organismo'
        verbose_name_plural = u'Organismos'

    def __unicode__(self):
        return self.nombre

class Usuario(models.Model):
    user = models.OneToOneField(User)
    codigo = models.AutoField(verbose_name='Codigo Autogenerado', primary_key=True)
    numero = models.IntegerField(verbose_name='Codigo' ,unique=True)
    nivel = models.ForeignKey(Nivel, verbose_name='nivel',)
    organismo = models.ForeignKey(Organismo, verbose_name='Organismo')
    dependencia = models.IntegerField(verbose_name='Dependencia',)
    nombres = models.CharField(verbose_name='Nombres', max_length=30,)
    apellidos = models.CharField(verbose_name='Apellidos', max_length=30,)
    sexo = models.CharField(verbose_name='sexo', max_length=2,choices = SEXO, )
    usuario = models.CharField(verbose_name='usuario', max_length=15,)
    email = models.EmailField(verbose_name='Email', max_length=135, unique=True)
    contrasena = models.CharField(verbose_name='contraseña', max_length=128)
    emailalt = models.EmailField(verbose_name='Email Alternativo', max_length=135,blank=True, null=True)
    fono = models.CharField(verbose_name='Telefono', max_length=25,)
    anexo = models.CharField(verbose_name='Anexo', max_length=10, default=0)
    rpm = models.CharField(verbose_name='Celular RPM', max_length=25, blank=True, null=True)
    rpc = models.CharField(verbose_name='Celular RPC', max_length=25, blank=True, null=True)
    nextel = models.CharField(verbose_name='Celular Nextel', max_length=25, blank=True, null=True)
    twitter = models.URLField(verbose_name='Cuenta Twitter', max_length=150, blank=True, null=True)
    facebook = models.URLField(verbose_name='Cuenta Facebook', max_length=150, blank=True, null=True)
    estado = models.ForeignKey(Estado, verbose_name='Estado',)
    politica = models.BooleanField(verbose_name='Acepto Politica de Uso',)
    idusuario_mod = models.IntegerField(verbose_name='Usuario modifico', null=True, blank=True)
    fec_mod = models.DateTimeField(verbose_name='Fecha modifico', auto_now=True, null=True, blank=True)
    foto = models.FileField(upload_to='users/',verbose_name='Foto', null=True, blank=True)

    def __init__(self, *args, **kw):
        super(Usuario, self).__init__(*args, **kw)
        self._dep = None

    class Meta:
        db_table = u'usuario'
        verbose_name = u'Usuario'
        verbose_name_plural = u'Usuarios'        
        permissions = (
            ('query_usuario','Puede Consultar Usuario'),
            ('add_admin','Puede Agregar Administrador'),
            ('change_admin','Puede Modificar Administrador'),
            ('delete_admin','Puede Eliminar Administrador'),
            ('query_admin','Puede Consultar Administrador'),
            ('asignar_permisos','Puede Asignar Permisos a Usuario'),
            #('asignar_permisos','Puede Asignar Permisos a Administrador'),
        )

    def __unicode__(self):
        return "%s, %s" % (self.nombres, self.apellidos)
    
    def get_dependencia(self):
        from dependencia.models import Gobernacion, Ministerio, Odp
        if self._dep:
            return self._dep
        else:
            if self.organismo.codigo == 1:
                self._dep= Ministerio.objects.get(nummin=self.dependencia)
            elif self.organismo.codigo == 2:
                self._dep= Odp.objects.get(numodp=self.dependencia)
            elif self.organismo.codigo == 3:
                self._dep= Gobernacion.objects.get(numgob=self.dependencia)
            return self._dep  
        
