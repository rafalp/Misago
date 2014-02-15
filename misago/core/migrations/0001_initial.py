# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'CacheVersion'
        db.create_table(u'core_cacheversion', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('cache', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('version', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
        ))
        db.send_create_signal(u'core', ['CacheVersion'])


    def backwards(self, orm):
        # Deleting model 'CacheVersion'
        db.delete_table(u'core_cacheversion')


    models = {
        u'core.cacheversion': {
            'Meta': {'object_name': 'CacheVersion'},
            'cache': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'version': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['core']
