# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Group'
        db.create_table(u'settings_group', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('key', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'settings', ['Group'])

        # Adding model 'Setting'
        db.create_table(u'settings_setting', (
            ('setting', self.gf('django.db.models.fields.CharField')(max_length=255, primary_key=True)),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['settings.Group'], to_field='key')),
            ('value', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('value_default', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('input', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('extra', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('position', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('separator', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'settings', ['Setting'])


    def backwards(self, orm):
        # Deleting model 'Group'
        db.delete_table(u'settings_group')

        # Deleting model 'Setting'
        db.delete_table(u'settings_setting')


    models = {
        u'settings.group': {
            'Meta': {'object_name': 'Group'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'settings.setting': {
            'Meta': {'object_name': 'Setting'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'extra': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['settings.Group']", 'to_field': "'key'"}),
            'input': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'position': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'separator': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'setting': ('django.db.models.fields.CharField', [], {'max_length': '255', 'primary_key': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'value': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'value_default': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['settings']