# -*- coding: utf-8 -*-
from django.db import models
from usuario.models import Organismo, Usuario,  Estado
from datetime import datetime
CATEGORIAS = (
    ('OTROS','OTROS'),
    ('IMAGENES','IMAGENES'),
    ('VIDEOS','VIDEOS'),
    ('AUDIOS','AUDIOS'),
    ('DOCUMENTOS','DOCUMENTOS'),
    ('COMPRIMIDOS','COMPRIMIDOS'),
)

EXTENSIONES = (
    ('OTROS',(
        ('OTRO','OTRO'),
        )
    ),
    ('IMAGENES',(
        ('JPG','JPG'),('GIF','GIF'),('ICO','ICO'),('PNG','PNG'),('TIF','TIF')
        )
    ),  
    ('VIDEOS',(
        ('AVI','AVI'),('MOV','MOV'),('MP4','MP4'),('WMV','WMV'),('FLV','FLV'),('F4V','F4V'),('3GP','3GP'),
        )
    ),
    ('AUDIOS',(
        ('MP3','MP3'),('WAV','WAV'),('AMF','AMF'),('AMV','AMV'),('OGG','OGG'),
        )
    ),
    ('DOCUMENTOS',(
        ('DOC','DOC'),('DOCX','DOCX'),('PDF','PDF'),('PPT','PPT'),('PPTX','PPTX'),('XLS','XLS'),('XLSX','XLSX'),('TXT','TXT'),('ODT','ODT'),
        )
    ),
    ('COMPRIMIDOS',(
        ('ZIP','ZIP'),('TAR','TAR'),('GZ','GZ'),('ZIP','ZIP'),('RAR','RAR'),('7Z','7Z'),
        )
    ),
)

class MaterialGrafico(models.Model):
    codigo = models.AutoField(verbose_name='Codigo Autoincrementado',primary_key=True)
    nummg = models.IntegerField(verbose_name='Numero de la MG', unique=True)
    organismo = models.ForeignKey(Organismo, verbose_name='Organismo')
    dependencia = models.IntegerField(verbose_name='Dependencia',)
    arcmg1 = models.FileField(verbose_name='Adjuntar Archivo 1',upload_to='materialgrafico/')
    urlmg1 = models.URLField(verbose_name='Url del MG',max_length=100,null=True,blank=True)
    arcmg2 = models.FileField(verbose_name='Adjuntar Archivo 2',upload_to='materialgrafico/',null=True,blank=True)
    urlmg2 = models.URLField(verbose_name='Url del MG',max_length=100,null=True,blank=True)
    arcmg3 = models.FileField(verbose_name='Adjuntar Archivo 3',upload_to='materialgrafico/',null=True,blank=True)
    urlmg3 = models.URLField(verbose_name='Url del MG',max_length=100,null=True,blank=True)
    arcmg4 = models.FileField(verbose_name='Adjuntar Archivo 4',upload_to='materialgrafico/',null=True,blank=True)
    urlmg4 = models.URLField(verbose_name='Url del MG',max_length=100,null=True,blank=True)
    arcmg5 = models.FileField(verbose_name='Adjuntar Archivo 5',upload_to='materialgrafico/',null=True,blank=True)
    urlmg5 = models.URLField(verbose_name='Url del MG',max_length=100,null=True,blank=True)
    arcmg6 = models.FileField(verbose_name='Adjuntar Archivo 6',upload_to='materialgrafico/',null=True,blank=True)
    urlmg6 = models.URLField(verbose_name='Url del MG',max_length=100,null=True,blank=True)
    arcmg7 = models.FileField(verbose_name='Adjuntar Archivo 7',upload_to='materialgrafico/',null=True,blank=True)
    urlmg7 = models.URLField(verbose_name='Url del MG',max_length=100,null=True,blank=True)
    arcmg8 = models.FileField(verbose_name='Adjuntar Archivo 8',upload_to='materialgrafico/',null=True,blank=True)
    urlmg8 = models.URLField(verbose_name='Url del MG',max_length=100,null=True,blank=True)
    idusuario_creac = models.IntegerField(verbose_name='Usuario creador',)
    fec_creac = models.DateTimeField(verbose_name='Fecha de creación del registro',auto_now_add=True)

    class Meta:
        db_table = u'materialgrafico'
        verbose_name = u'MG'
        verbose_name_plural = u'MGs'
        permissions = (
            ('query_materialgrafico','Puede Consultar MG'),
        )

    def __unicode__(self):
        return self.nummg


class DocumentoInteresGeneral(models.Model):
    codigo = models.AutoField(verbose_name='Codigo Autoincrementado',primary_key=True)
    numdig = models.IntegerField(verbose_name='Numero de la DIG', unique=True)
    organismo = models.ForeignKey(Organismo, verbose_name='Organismo')
    dependencia = models.IntegerField(verbose_name='Dependencia',)
    archmis1 = models.FileField(verbose_name='Adjuntar Archivo 1',upload_to='documentosgeneral/mis/')
    urlmis1 = models.URLField(verbose_name='Url del DIG',max_length=100,null=True,blank=True)
    archmis2 = models.FileField(verbose_name='Adjuntar Archivo 2',upload_to='documentosgeneral/mis/',null=True,blank=True)
    urlmis2 = models.URLField(verbose_name='Url del DIG',max_length=100,null=True,blank=True)
    archmis3 = models.FileField(verbose_name='Adjuntar Archivo 3',upload_to='documentosgeneral/mis/',null=True,blank=True)
    urlmis3 = models.URLField(verbose_name='Url del DIG',max_length=100,null=True,blank=True)
    archaca1 = models.FileField(verbose_name='Adjuntar Archivo 1',upload_to='documentosgeneral/aca/')
    urlaca1 = models.URLField(verbose_name='Url del DIG',max_length=100,null=True,blank=True)
    archaca2 =  models.FileField(verbose_name='Adjuntar Archivo 2',upload_to='documentosgeneral/aca/',null=True,blank=True)
    urlaca2 = models.URLField(verbose_name='Url del DIG',max_length=100,null=True,blank=True)
    archaca3 =  models.FileField(verbose_name='Adjuntar Archivo 3',upload_to='documentosgeneral/aca/',null=True,blank=True)
    urlaca3 = models.URLField(verbose_name='Url del DIG',max_length=100,null=True,blank=True)
    archbue1 =  models.FileField(verbose_name='Adjuntar Archivo 1',upload_to='documentosgeneral/bue/')
    urlbue1 = models.URLField(verbose_name='Url del DIG',max_length=100,null=True,blank=True)
    archbue2 =  models.FileField(verbose_name='Adjuntar Archivo 2',upload_to='documentosgeneral/bue/',null=True,blank=True)
    urlbue2 = models.URLField(verbose_name='Url del DIG',max_length=100,null=True,blank=True)
    archbue3 =  models.FileField(verbose_name='Adjuntar Archivo 3',upload_to='documentosgeneral/bue/',null=True,blank=True)
    urlbue3 = models.URLField(verbose_name='Url del DIG',max_length=100,null=True,blank=True)
    idusuario_creac = models.IntegerField(verbose_name='Usuario creador',)
    fec_creac = models.DateTimeField(verbose_name='Fecha de creación del registro',auto_now_add=True)

    class Meta:
        db_table = u'documentointeresgeneral'
        verbose_name = u'DIG'
        verbose_name_plural = u'DIGs'
        permissions = (
            ('query_documentointeresgeneral','Puede Consultar DIG'),
        )

    def __unicode__(self):
        return self.numdig

	
class ActaReunionIntersectorial(models.Model):
    codigo = models.AutoField(verbose_name='Codigo Autoincrementado',primary_key=True)
    numari = models.IntegerField(verbose_name='Numero de la ARI', unique=True)
    organismo = models.ForeignKey(Organismo, verbose_name='Organismo')
    dependencia = models.IntegerField(verbose_name='Dependencia',)
    nombreari = models.CharField(verbose_name='Nombre de la Reunión', max_length=150)
    archari = models.FileField(verbose_name='Adjuntar Archivo',upload_to='actas/')
    urlari = models.URLField(verbose_name='Url de la Acta',max_length=100,null=True,blank=True)
    idusuario_creac = models.IntegerField(verbose_name='Usuario creador',)
    fec_creac = models.DateTimeField(verbose_name='Fecha de creación del registro',auto_now_add=True)

    class Meta:
        db_table = u'actareunionintersectorial'
        verbose_name = u'ARI'
        verbose_name_plural = u'ARIs'
        permissions = (
            ('query_actareunionintersectorial','Puede Consultar ARI'),
        )

    def __unicode__(self):
        return self.nombreari

class Documento(models.Model):
    codigo = models.AutoField(verbose_name='Codigo', primary_key=True)
    organismo = models.ForeignKey(Organismo, verbose_name='Organismo')
    dependencia = models.IntegerField(verbose_name='Dependencia',)
    archivo = models.FileField(verbose_name ='Adjuntar Archivo', upload_to='documentos')
    fecha = models.DateField(verbose_name='Fecha del documento',default=datetime.today())#NEW
    descripcion = models.TextField(verbose_name='Descripción',)#NEW
    estado = models.ForeignKey(Estado, verbose_name='Estado', default=1)
    url_archivo = models.URLField(verbose_name='URL del Archivo',null=True, blank=True)
    tipo = models.CharField(verbose_name = 'Tipo',max_length=5,choices=EXTENSIONES)
    categoria = models.CharField(verbose_name = 'Categoria',choices=CATEGORIAS,max_length=50)
    idusuario_creac = models.ForeignKey(Usuario, verbose_name='Usuario',)
    fec_creac = models.DateTimeField(verbose_name='Fecha de creación del registro',auto_now_add=True)
    idusuario_mod = models.ForeignKey(Usuario,verbose_name='Usuario modifico',
    related_name='modificador_documentos', null=True, blank=True)
    fec_mod = models.DateTimeField(verbose_name='Fecha modifico', null=True, blank=True)
    idadministrador_mod = models.ForeignKey(Usuario,verbose_name='Usuario modifico',
    related_name='adminmod_documentos', null=True, blank=True)
    fec_modadm = models.DateTimeField(verbose_name='Fecha modifico', null=True, blank=True)
    class Meta:
        db_table = u'documentos'
        verbose_name = u'Documento'
        verbose_name_plural = u'Documentos'
        permissions = (
            ('query_documento','Puede Consultar Documento'),
        )

    def __unicode__(self):
        return self.archivo
