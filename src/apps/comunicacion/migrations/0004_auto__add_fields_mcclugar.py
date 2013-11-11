# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models
from ubigeo.models import Distrito

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Oac.estado'
        db.add_column(u'mcc_lugar', 'distrito', models.ForeignKey(Distrito,
        	related_name='lugares', null=True,blank=True), keep_default=False)
        
    def backwards(self, orm):
        
        # Deleting field 'Oac.estado'
        pass