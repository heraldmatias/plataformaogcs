# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models
from usuario.models import Estado, Usuario

class Migration(SchemaMigration):

    def forwards(self, orm):        
        # Adding field 'documentos.estado'          
        db.add_column(u'usuario', 'idusuario_creac', models.ForeignKey(Usuario,
        	related_name='creador', to_field='numero',null=True,blank=True), keep_default=False)       
        db.add_column(u'usuario', 'fec_creac', models.DateTimeField(null=True,blank=True), keep_default=False)        
        db.rename_column('usuario', 'idusuario_mod', 'idusuario_mod_id')
        db.alter_column('usuario', 'idusuario_mod_id', models.ForeignKey(Usuario,
            related_name='modificador', to_field='numero',
            null=True,blank=True))
    def backwards(self, orm):        
        # Deleting field 'documentos.estado'
        db.delete_column(u'usuario', 'idusuario_creac_id')