# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'SettingsGroup'
        db.create_table(u'conf_settingsgroup', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('key', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'conf', ['SettingsGroup'])

        # Adding model 'Setting'
        db.create_table(u'conf_setting', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['conf.SettingsGroup'])),
            ('setting', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('legend', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('order', self.gf('django.db.models.fields.IntegerField')(default=0, db_index=True)),
            ('dry_value', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('default_value', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('python_type', self.gf('django.db.models.fields.CharField')(default='string', max_length=255)),
            ('is_lazy', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('form_field', self.gf('django.db.models.fields.CharField')(default='text', max_length=255)),
            ('pickled_field_extra', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'conf', ['Setting'])


    def backwards(self, orm):
        # Deleting model 'SettingsGroup'
        db.delete_table(u'conf_settingsgroup')

        # Deleting model 'Setting'
        db.delete_table(u'conf_setting')


    models = {
        u'conf.setting': {
            'Meta': {'object_name': 'Setting'},
            'default_value': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'dry_value': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'form_field': ('django.db.models.fields.CharField', [], {'default': "'text'", 'max_length': '255'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['conf.SettingsGroup']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_lazy': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'legend': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_index': 'True'}),
            'pickled_field_extra': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'python_type': ('django.db.models.fields.CharField', [], {'default': "'string'", 'max_length': '255'}),
            'setting': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'conf.settingsgroup': {
            'Meta': {'object_name': 'SettingsGroup'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['conf']
