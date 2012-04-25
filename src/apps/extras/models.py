# -*- coding: utf-8 -*-
from django.db import models

class MaterialGrafico(models.Model):
    codigo = models.AutoField(verbose_name='Codigo Autoincrementado',primary_key=True)
    nummg = models.IntegerField(verbose_name='Numero de la MG', unique=True)
    urlmg1 = models.FileField(verbose_name='Adjuntar Archivo 1',upload_to='materialgrafico/')
    urlmg2 = models.FileField(verbose_name='Adjuntar Archivo 2',upload_to='materialgrafico/')
    urlmg3 = models.FileField(verbose_name='Adjuntar Archivo 3',upload_to='materialgrafico/')
    urlmg4 = models.FileField(verbose_name='Adjuntar Archivo 4',upload_to='materialgrafico/')
    urlmg5 = models.FileField(verbose_name='Adjuntar Archivo 5',upload_to='materialgrafico/')
    urlmg6 = models.FileField(verbose_name='Adjuntar Archivo 6',upload_to='materialgrafico/')
    urlmg7 = models.FileField(verbose_name='Adjuntar Archivo 7',upload_to='materialgrafico/')
    urlmg8 = models.FileField(verbose_name='Adjuntar Archivo 8',upload_to='materialgrafico/')
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
    urlmis1 = models.FileField(verbose_name='Adjuntar Archivo 1',upload_to='documentosgeneral/mis/')
    urlmis2 = models.FileField(verbose_name='Adjuntar Archivo 2',upload_to='documentosgeneral/mis/')
    urlmis3 = models.FileField(verbose_name='Adjuntar Archivo 3',upload_to='documentosgeneral/mis/')
    urlaca1 = models.FileField(verbose_name='Adjuntar Archivo 1',upload_to='documentosgeneral/aca/')
    urlaca2 = models.FileField(verbose_name='Adjuntar Archivo 2',upload_to='documentosgeneral/aca/')
    urlaca3 = models.FileField(verbose_name='Adjuntar Archivo 3',upload_to='documentosgeneral/aca/')
    urlbue1 = models.FileField(verbose_name='Adjuntar Archivo 1',upload_to='documentosgeneral/bue/')
    urlbue2 = models.FileField(verbose_name='Adjuntar Archivo 2',upload_to='documentosgeneral/bue/')
    urlbue3 = models.FileField(verbose_name='Adjuntar Archivo 3',upload_to='documentosgeneral/bue/')
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
    urlari = models.FileField(verbose_name='Adjuntar Archivo',upload_to='actas/')
    idusuario_creac = models.IntegerField(verbose_name='Usuario creador',)
    fec_creac = models.DateTimeField(verbose_name='Fecha de creación del registro',auto_now_add=True)

    class Meta:
        db_table = u'actareunionintersectorial'
        verbose_name = u'Acta Reunion Intersectorial'
        verbose_name_plural = u'Actas de Reunion Intersectorial'

    def __unicode__(self):
        return self.nombreari

