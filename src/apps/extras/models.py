# -*- coding: utf-8 -*-
from django.db import models
from usuario.models import Organismo

class MaterialGrafico(models.Model):
    codigo = models.AutoField(verbose_name='Codigo Autoincrementado',primary_key=True)
    nummg = models.IntegerField(verbose_name='Numero de la MG', unique=True)
    organismo = models.ForeignKey(Organismo, verbose_name='Organismo')
    dependencia = models.IntegerField(verbose_name='Dependencia',)
    arcmg1 = models.FileField(verbose_name='Adjuntar Archivo 1',upload_to='materialgrafico/')
    urlmg1 = models.URLField(verbose_name='Url de la oac',max_length=100,null=True,blank=True)
    arcmg2 = models.FileField(verbose_name='Adjuntar Archivo 2',upload_to='materialgrafico/')
    urlmg2 = models.URLField(verbose_name='Url de la oac',max_length=100,null=True,blank=True)
    arcmg3 = models.FileField(verbose_name='Adjuntar Archivo 3',upload_to='materialgrafico/')
    urlmg3 = models.URLField(verbose_name='Url de la oac',max_length=100,null=True,blank=True)
    arcmg4 = models.FileField(verbose_name='Adjuntar Archivo 4',upload_to='materialgrafico/')
    urlmg4 = models.URLField(verbose_name='Url de la oac',max_length=100,null=True,blank=True)
    arcmg5 = models.FileField(verbose_name='Adjuntar Archivo 5',upload_to='materialgrafico/')
    urlmg5 = models.URLField(verbose_name='Url de la oac',max_length=100,null=True,blank=True)
    arcmg6 = models.FileField(verbose_name='Adjuntar Archivo 6',upload_to='materialgrafico/')
    urlmg6 = models.URLField(verbose_name='Url de la oac',max_length=100,null=True,blank=True)
    arcmg7 = models.FileField(verbose_name='Adjuntar Archivo 7',upload_to='materialgrafico/')
    urlmg7 = models.URLField(verbose_name='Url de la oac',max_length=100,null=True,blank=True)
    arcmg8 = models.FileField(verbose_name='Adjuntar Archivo 8',upload_to='materialgrafico/')
    urlmg8 = models.URLField(verbose_name='Url de la oac',max_length=100,null=True,blank=True)
    idusuario_creac = models.IntegerField(verbose_name='Usuario creador',)
    fec_creac = models.DateTimeField(verbose_name='Fecha de creación del registro',auto_now_add=True)

    class Meta:
        db_table = u'materialgrafico'
        verbose_name = u'Material Grafico'
        verbose_name_plural = u'Materiales Graficos'

    def __unicode__(self):
        return self.nummg


class DocumentoInteresGeneral(models.Model):
    codigo = models.AutoField(verbose_name='Codigo Autoincrementado',primary_key=True)
    numdig = models.IntegerField(verbose_name='Numero de la DIG', unique=True)
    archmis1 = models.FileField(verbose_name='Adjuntar Archivo 1',upload_to='documentosgeneral/mis/')
    urlmis1 = models.URLField(verbose_name='Url de la oac',max_length=100,null=True,blank=True)
    archmis2 = models.FileField(verbose_name='Adjuntar Archivo 1',upload_to='documentosgeneral/mis/')
    urlmis2 = models.URLField(verbose_name='Url de la oac',max_length=100,null=True,blank=True)
    archmis3 = models.FileField(verbose_name='Adjuntar Archivo 1',upload_to='documentosgeneral/mis/')
    urlmis3 = models.URLField(verbose_name='Url de la oac',max_length=100,null=True,blank=True)
    archaca1 = models.FileField(verbose_name='Adjuntar Archivo 1',upload_to='documentosgeneral/mis/')
    urlaca1 = models.URLField(verbose_name='Url de la oac',max_length=100,null=True,blank=True)
    archaca2 =  models.FileField(verbose_name='Adjuntar Archivo 1',upload_to='documentosgeneral/mis/')
    urlaca2 = models.URLField(verbose_name='Url de la oac',max_length=100,null=True,blank=True)
    archaca3 =  models.FileField(verbose_name='Adjuntar Archivo 1',upload_to='documentosgeneral/mis/')
    urlaca3 = models.URLField(verbose_name='Url de la oac',max_length=100,null=True,blank=True)
    archbue1 =  models.FileField(verbose_name='Adjuntar Archivo 1',upload_to='documentosgeneral/mis/')
    urlbue1 = models.URLField(verbose_name='Url de la oac',max_length=100,null=True,blank=True)
    archbue2 =  models.FileField(verbose_name='Adjuntar Archivo 1',upload_to='documentosgeneral/mis/')
    urlbue2 = models.URLField(verbose_name='Url de la oac',max_length=100,null=True,blank=True)
    archbue3 =  models.FileField(verbose_name='Adjuntar Archivo 1',upload_to='documentosgeneral/mis/')
    urlbue3 = models.URLField(verbose_name='Url de la oac',max_length=100,null=True,blank=True)
    idusuario_creac = models.IntegerField(verbose_name='Usuario creador',)
    fec_creac = models.DateTimeField(verbose_name='Fecha de creación del registro',auto_now_add=True)

    class Meta:
        db_table = u'documentointeresgeneral'
        verbose_name = u'Documento Interes General'
        verbose_name_plural = u'Documentos Interes General'

    def __unicode__(self):
        return self.numdig

	
class ActaReunionIntersectorial(models.Model):
    codigo = models.AutoField(verbose_name='Codigo Autoincrementado',primary_key=True)
    numari = models.IntegerField(verbose_name='Numero de la ARI', unique=True)
    nombreari = models.CharField(verbose_name='Nombre de la ARI', max_length=150)
    archari = models.FileField(verbose_name='Adjuntar Archivo',upload_to='actas/')
    urlari = models.URLField(verbose_name='Url de la Acta',max_length=100,null=True,blank=True)
    idusuario_creac = models.IntegerField(verbose_name='Usuario creador',)
    fec_creac = models.DateTimeField(verbose_name='Fecha de creación del registro',auto_now_add=True)

    class Meta:
        db_table = u'actareunionintersectorial'
        verbose_name = u'Acta Reunion Intersectorial'
        verbose_name_plural = u'Actas de Reunion Intersectorial'

    def __unicode__(self):
        return self.nombreari

