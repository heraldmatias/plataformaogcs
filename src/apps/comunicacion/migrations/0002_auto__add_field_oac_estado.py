# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models
from usuario.models import Estado

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Oac.estado'
        db.add_column(u'oac', 'estado', models.ForeignKey(Estado,default=1), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Oac.estado'
        db.delete_column(u'oac', 'estado_id')