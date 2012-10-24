# -*- coding: utf-8 -*-
from django.db import models
from usuario.models import Estado, Organismo, Usuario
from datetime import datetime
# Dependencia (automaticamente del usuario creador) , Descripcion, Fecha , Archivo y Estado.
#En las nuevas opciones de "Resumenes de Prensa" y 
#"Caso de Exito" solo se podrán subir archivos con las extensiones 
#PDF, DOC, PPT, JPG, GIF y PNG.  
class PrensaBase(models.Model):
    codigo = models.AutoField(verbose_name='Código', primary_key=True)
    organismo = models.ForeignKey(Organismo, verbose_name='Organismo')
    dependencia = models.IntegerField(verbose_name='Dependencia',)    
    fecha = models.DateField(verbose_name='Fecha Resumen Prensa',default=datetime.today())    
    descripcion = models.TextField(verbose_name='Descripción',)
    
    class Meta:
        abstract = True

class ResumenPrensa(PrensaBase):
    estado = models.ForeignKey(Estado, related_name="rep_estado", verbose_name='Estado',default=1)
    archivo = models.FileField(verbose_name='Adjuntar Archivo',upload_to='prensa/resumenes/')
    idusuario_creac = models.ForeignKey(Usuario,related_name="rep_userc",verbose_name='Usuario creador',to_field='numero')
    fec_creac = models.DateTimeField(verbose_name='Fecha de creación del registro',auto_now_add=True)
    idusuario_mod = models.ForeignKey(Usuario,related_name="rep_userm",verbose_name='Usuario creador',
        to_field='numero',null=True,blank=True)
    fec_mod = models.DateTimeField(verbose_name='Fecha modifico', null=True, blank=True)

    class Meta:
        db_table = u'tbl_resumen_prensa'
        verbose_name = u'Resumen Prensa'
        verbose_name_plural = u'Resumenes de Prensa'
        permissions = (
            ('query_resumen_prensa','Puede Consultar Resumen'),
        )

    def __unicode__(self):
        return self.archivo

class CasoExito(PrensaBase):
    estado = models.ForeignKey(Estado, related_name="ce_estado", verbose_name='Estado', default=1)
    archivo = models.FileField(verbose_name='Adjuntar Archivo',upload_to='prensa/casos_exito/')    
    idusuario_creac = models.ForeignKey(Usuario,related_name="ce_userc",verbose_name='Usuario creador',to_field='numero')
    fec_creac = models.DateTimeField(verbose_name='Fecha de creación del registro',auto_now_add=True)
    idusuario_mod = models.ForeignKey(Usuario,related_name="ce_userm",verbose_name='Usuario creador',
        to_field='numero',null=True,blank=True)
    fec_mod = models.DateTimeField(verbose_name='Fecha modifico', null=True, blank=True)

    class Meta:
        db_table = u'tbl_caso_exito'
        verbose_name = u'Caso de Éxito'
        verbose_name_plural = u'Casos de Éxito'
        permissions = (
            ('query_caso_exito','Puede Consultar Caso Exito'),
        )

    def __unicode__(self):
        return self.archivo