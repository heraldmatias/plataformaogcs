# -*- coding: utf-8 -*-

from django.db import models
from usuario.models import Estado

class Region(models.Model):
    codigo = models.AutoField(verbose_name='Codigo', primary_key=True)
    #numreg = models.IntegerField(verbose_name='Numero de la región', unique=True)
    numreg = models.IntegerField(verbose_name='Numero de la región')
    region = models.CharField(verbose_name='Región',unique=True, max_length=70)
    estado = models.ForeignKey(Estado, verbose_name='Estado',)
    idusuario_creac = models.IntegerField(verbose_name='Numero del Usuario de creación')
    fec_creac = models.DateTimeField(verbose_name='Fecha de creación del registro', auto_now_add=True)
    idusuario_mod = models.IntegerField(verbose_name='Numero del Usuario de modificación', blank=True, null=True)
    fec_mod = models.DateTimeField(verbose_name='Fecha de modificación del registro', auto_now=True)
    
    class Meta:
        db_table = u'region'
        verbose_name = u'Región'
        verbose_name_plural = u'Regiones'
        permissions = (
            ('query_region','Puede Consultar Region'),
        )

    def __unicode__(self):
        return self.region     

class Provincia(models.Model):
    codigo = models.AutoField(verbose_name='Codigo', primary_key=True)
    #numpro = models.IntegerField(verbose_name='Numero de la provincia', unique=True)
    numpro = models.IntegerField(verbose_name='Numero de la provincia')
    region = models.ForeignKey(Region, verbose_name='Región', max_length=70, related_name='fpr')
    provincia = models.CharField(verbose_name='Provincia', max_length=70,)
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
        permissions = (
            ('query_provincia','Puede Consultar Provincia'),
        )
  
    def __unicode__(self):
        return self.provincia

class Distrito(models.Model):
    codigo = models.AutoField(verbose_name='Codigo', primary_key=True)
    #numdis = models.IntegerField(verbose_name='Numero del distrito', unique=True)
    numdis = models.IntegerField(verbose_name='Numero del distrito')
    provincia = models.ForeignKey(Provincia, verbose_name='Provincia', max_length=70)
    region = models.ForeignKey(Region, verbose_name='Región', max_length=70, related_name='fdr')
    distrito = models.CharField(verbose_name='Distrito', max_length=70,)
    estado = models.ForeignKey(Estado, verbose_name='Estado')
    idusuario_creac = models.IntegerField(verbose_name='Numero del Usuario de creación', blank=True, null=True)
    fec_creac = models.DateTimeField(verbose_name='Fecha de creación del registro', auto_now_add=True, blank=True, null=True)
    idusuario_mod = models.IntegerField(verbose_name='Numero del Usuario de modificación', blank=True, null=True)
    fec_mod = models.DateTimeField(verbose_name='Fecha de modificación del registro', auto_now=True, blank=True, null=True)

    class Meta:
        db_table = u'distrito'
        verbose_name = u'Distrito'
        verbose_name_plural = u'Distritos'
        unique_together = ('region','provincia','distrito')
        permissions = (
            ('query_distrito','Puede Consultar Distrito'),
        )

    def __unicode__(self):
        return self.distrito