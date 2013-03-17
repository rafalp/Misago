# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Ban'
        db.create_table(u'banning_ban', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('ban', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('reason_user', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('reason_admin', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('expires', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'banning', ['Ban'])


    def backwards(self, orm):
        # Deleting model 'Ban'
        db.delete_table(u'banning_ban')


    models = {
        u'banning.ban': {
            'Meta': {'object_name': 'Ban'},
            'ban': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'expires': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'reason_admin': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'reason_user': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['banning']