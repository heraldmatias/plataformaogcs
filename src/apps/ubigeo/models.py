# -*- coding: utf-8 -*-

from django.db import models
from usuario.models import Estado

class Region(models.Model):
    codigo = models.AutoField(verbose_name='Codigo', primary_key=True)
    numreg = models.IntegerField(verbose_name='Numero de la región', unique=True)
    region = models.CharField(verbose_name='Nombre de la región',unique=True, max_length=70)
    estado = models.ForeignKey(Estado, verbose_name='Estado',)
    idusuario_creac = models.IntegerField(verbose_name='Numero del Usuario de creación')
    fec_creac = models.DateTimeField(verbose_name='Fecha de creación del registro', auto_now_add=True)
    idusuario_mod = models.IntegerField(verbose_name='Numero del Usuario de modificación', blank=True, null=True)
    fec_mod = models.DateTimeField(verbose_name='Fecha de modificación del registro', auto_now=True)
    
    class Meta:
        db_table = u'region'
        verbose_name = u'Región'
        verbose_name_plural = u'Regiones'
    
    def __unicode__(self):
        return self.region     

class Provincia(models.Model):
    codigo = models.AutoField(verbose_name='Codigo', primary_key=True)
    numpro = models.IntegerField(verbose_name='Numero de la provincia', unique=True)
    region = models.ForeignKey(Region, verbose_name='Nombre de la región', max_length=70, to_field='numreg')
    provincia = models.CharField(verbose_name='Nombre de la provincia', max_length=70,)
    estado = models.ForeignKey(Estado, verbose_name='Estado')
    idusuario_creac = models.IntegerField(verbose_name='Numero del Usuario de creación', blank=True, null=True)
    fec_creac = models.DateTimeField(verbose_name='Fecha de creación del registro', auto_now_add=True, blank=True, null=True)
    idusuario_mod = models.IntegerField(verbose_name='Numero del Usuario de modificación', blank=True, null=True)
    fec_mod = models.DateTimeField(verbose_name='Fecha de modificación del registro', auto_now=True, blank=True, null=True)
    
    class Meta:
        db_table = u'provincia'
        verbose_name = u'Provincia'
        verbose_name_plural = u'Provincias'
        unique_together = ('region','provincia',)
  
    def __unicode__(self):
        return self.provincia
