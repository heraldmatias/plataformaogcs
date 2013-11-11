# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models
from usuario.models import Estado, Usuario

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Oac.estado'
        db.delete_column(u'mcc', 'nummccestado_id')
        db.delete_column(u'mcc', 'propuestamcc')
        db.add_column(u'mcc', 'mensajes', models.TextField(null=True, blank=True), keep_default=False)
        db.add_column(u'mcc', 'cuestionamientos', models.TextField(null=True, blank=True), keep_default=False)
        
    def backwards(self, orm):
        
        # Deleting field 'Oac.estado'
        pass