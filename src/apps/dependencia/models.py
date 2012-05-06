# -*- coding: utf-8 -*-

from django.db import models
from usuario.models import Estado
from ubigeo.models import Region, Provincia

class Ministerio(models.Model):
    codigo = models.AutoField(verbose_name='Codigo', primary_key=True)
    nummin = models.IntegerField(verbose_name='Numero', unique=True)
    ministerio = models.CharField(verbose_name='Ministerio', max_length=70,unique=True)
    iniciales = models.CharField(verbose_name='Iniciales', max_length=15,unique=True) 
    estado = models.ForeignKey(Estado, verbose_name='Estado')
    idusuario_creac = models.IntegerField(verbose_name='Numero del Usuario de creación', blank=True, null=True)
    fec_creac = models.DateTimeField(verbose_name='Fecha de creación del registro', auto_now_add=True, blank=True, null=True)
    idusuario_mod = models.IntegerField(verbose_name='Numero del Usuario de modificación', blank=True, null=True)
    fec_mod = models.DateTimeField(verbose_name='Fecha de modificación del registro', auto_now=True, blank=True, null=True)

    class Meta:
        db_table = u'ministerio'
        verbose_name = u'Ministerio'
        verbose_name_plural = u'Ministerios'
        
    def __unicode__(self):
        return self.ministerio

class Odp(models.Model):
    codigo = models.AutoField(verbose_name='Codigo', primary_key=True)
    numodp = models.IntegerField(verbose_name='Numero', unique=True)
    nummin = models.ForeignKey(Ministerio, verbose_name='Ministerio', to_field='nummin')
    odp = models.CharField(verbose_name='ODP', max_length=70, unique=True)
    iniciales = models.CharField(verbose_name='Iniciales', max_length=15, unique=True) 
    estado = models.ForeignKey(Estado, verbose_name='Estado')
    idusuario_creac = models.IntegerField(verbose_name='Numero del Usuario de creación', blank=True, null=True)
    fec_creac = models.DateTimeField(verbose_name='Fecha de creación del registro', auto_now_add=True, blank=True, null=True)
    idusuario_mod = models.IntegerField(verbose_name='Numero del Usuario de modificación', blank=True, null=True)
    fec_mod = models.DateTimeField(verbose_name='Fecha de modificación del registro', auto_now=True, blank=True, null=True)

    class Meta:
        db_table = u'odp'
        verbose_name = u'Odp'
        verbose_name_plural = u'Opds'
        
    def __unicode__(self):
        return self.odp

class Gobernacion(models.Model):
    codigo = models.AutoField(verbose_name='Codigo', primary_key=True)
    numgob = models.IntegerField(verbose_name='Numero', unique=True)
    region = models.ForeignKey(Region, verbose_name='Region', to_field='numreg',)
    provincia = models.ForeignKey(Provincia, verbose_name='Provincia', to_field='numpro')
    gobernacion = models.CharField(verbose_name='Gobernación', max_length=70,unique=True)
    iniciales = models.CharField(verbose_name='Iniciales', max_length=15,unique=True) 
    estado = models.ForeignKey(Estado, verbose_name='Estado')
    idusuario_creac = models.IntegerField(verbose_name='Numero del Usuario de creación', blank=True, null=True)
    fec_creac = models.DateTimeField(verbose_name='Fecha de creación del registro', auto_now_add=True, blank=True, null=True)
    idusuario_mod = models.IntegerField(verbose_name='Numero del Usuario de modificación', blank=True, null=True)
    fec_mod = models.DateTimeField(verbose_name='Fecha de modificación del registro', auto_now=True, blank=True, null=True)

    class Meta:
        db_table = u'gobernacion'
        verbose_name = u'Gobernación'
        verbose_name_plural = u'Gobernaciones'
        
    def __unicode__(self):
        return self.gobernacion

