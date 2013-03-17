# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Item'
        db.create_table(u'monitor_item', (
            ('id', self.gf('django.db.models.fields.CharField')(max_length=255, primary_key=True)),
            ('value', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'monitor', ['Item'])


    def backwards(self, orm):
        # Deleting model 'Item'
        db.delete_table(u'monitor_item')


    models = {
        u'monitor.item': {
            'Meta': {'object_name': 'Item'},
            'id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'primary_key': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'value': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['monitor']