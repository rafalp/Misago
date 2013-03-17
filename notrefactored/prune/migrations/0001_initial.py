# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Policy'
        db.create_table(u'prune_policy', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('email', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('posts', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('registered', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('last_visit', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
        ))
        db.send_create_signal(u'prune', ['Policy'])


    def backwards(self, orm):
        # Deleting model 'Policy'
        db.delete_table(u'prune_policy')


    models = {
        u'prune.policy': {
            'Meta': {'object_name': 'Policy'},
            'email': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_visit': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'posts': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'registered': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['prune']