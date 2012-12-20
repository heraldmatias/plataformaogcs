# encoding: utf-8
from south.db import db
from south.v2 import SchemaMigration
from django.db import models
from usuario.models import Usuario

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Oac.estado'        
        db.rename_column('ministerio', 'idusuario_creac', 'idusuario_creac_id')
        db.alter_column('ministerio', 'idusuario_creac_id', models.ForeignKey(Usuario,
            related_name='cministerio', to_field='numero',
            null=True,blank=True))
        db.rename_column(u'ministerio', 'idusuario_mod', 'idusuario_mod_id')
        db.alter_column('ministerio', 'idusuario_mod_id', models.ForeignKey(Usuario,
            related_name='eministerio', to_field='numero',
            null=True,blank=True))

        db.rename_column('odp', 'idusuario_creac', 'idusuario_creac_id')
        db.alter_column('odp', 'idusuario_creac_id', models.ForeignKey(Usuario,
            related_name='codp', to_field='numero',
            null=True,blank=True))
        db.rename_column(u'odp', 'idusuario_mod', 'idusuario_mod_id')
        db.alter_column('odp', 'idusuario_mod_id', models.ForeignKey(Usuario,
            related_name='eodp', to_field='numero',
            null=True,blank=True))

        db.rename_column('gobernacion', 'idusuario_creac', 'idusuario_creac_id')
        db.alter_column('gobernacion', 'idusuario_creac_id', models.ForeignKey(Usuario,
            related_name='cgobernacion', to_field='numero',
            null=True,blank=True))
        db.rename_column(u'gobernacion', 'idusuario_mod', 'idusuario_mod_id')
        db.alter_column('gobernacion', 'idusuario_mod_id', models.ForeignKey(Usuario,
            related_name='egobernacions', to_field='numero',
            null=True,blank=True))