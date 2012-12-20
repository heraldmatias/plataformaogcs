# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models
from usuario.models import Estado, Usuario

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Oac.estado'
        db.add_column(u'oac', 'estado', models.ForeignKey(Estado,default=1), keep_default=False)
        db.rename_column('oac', 'idusuario_creac', 'idusuario_creac_id')
        db.alter_column('oac', 'idusuario_creac_id', models.ForeignKey(Usuario,
            related_name='creador_oac', to_field='numero'))
        db.add_column(u'oac', 'idusuario_mod', models.ForeignKey(Usuario,
        	related_name='modificador_oac', to_field='numero',null=True,blank=True), keep_default=False)
        db.add_column(u'oac', 'fec_mod', models.DateTimeField(null=True,blank=True), keep_default=False)
        db.add_column(u'oac', 'idadministrador_mod', models.ForeignKey(Usuario,
        	related_name='adminmod_oac', to_field='numero',null=True,blank=True), keep_default=False)
        db.add_column(u'oac', 'fec_modadm', models.DateTimeField(null=True,blank=True), keep_default=False)
        db.rename_column('pgcs', 'idusuario_creac', 'idusuario_creac_id')
        db.alter_column('pgcs', 'idusuario_creac_id', models.ForeignKey(Usuario,
            to_field='numero',
            related_name='upgcs',null=True,blank=True))
        
    def backwards(self, orm):
        
        # Deleting field 'Oac.estado'
        db.delete_column(u'oac', 'estado_id')