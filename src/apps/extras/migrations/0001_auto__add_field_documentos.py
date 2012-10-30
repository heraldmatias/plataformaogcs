# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models
from usuario.models import Estado, Usuario

class Migration(SchemaMigration):

    def forwards(self, orm):        
        # Adding field 'documentos.estado'
        db.add_column(u'documentos', 'descripcion', models.TextField(null=True,blank=True), keep_default=False)
        db.add_column(u'documentos', 'fecha', models.DateField(null=True,blank=True), keep_default=False)
        db.add_column(u'documentos', 'estado', models.ForeignKey(Estado,default=1), keep_default=False)        
        db.add_column(u'documentos', 'idusuario_mod', models.ForeignKey(Usuario,
        	related_name='modificador_documentos', to_field='numero',null=True,blank=True), keep_default=False)
        db.add_column(u'documentos', 'fec_mod', models.DateTimeField(null=True,blank=True), keep_default=False)
        db.add_column(u'documentos', 'idadministrador_mod', models.ForeignKey(Usuario,
        	related_name='adminmod_documentos', to_field='numero',null=True,blank=True), keep_default=False)
        db.add_column(u'documentos', 'fec_modadm', models.DateTimeField(null=True,blank=True), keep_default=False)        
        
    def backwards(self, orm):
        
        # Deleting field 'documentos.estado'
        db.delete_column(u'documentos', 'estado_id')