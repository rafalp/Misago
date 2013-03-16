# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Fixture'
        db.create_table(u'setup_fixture', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('app_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'setup', ['Fixture'])


    def backwards(self, orm):
        # Deleting model 'Fixture'
        db.delete_table(u'setup_fixture')


    models = {
        u'setup.fixture': {
            'Meta': {'object_name': 'Fixture'},
            'app_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['setup']