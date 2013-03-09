# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ThemeAdjustment'
        db.create_table(u'themes_themeadjustment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('theme', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('useragents', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'themes', ['ThemeAdjustment'])


    def backwards(self, orm):
        # Deleting model 'ThemeAdjustment'
        db.delete_table(u'themes_themeadjustment')


    models = {
        u'themes.themeadjustment': {
            'Meta': {'object_name': 'ThemeAdjustment'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'theme': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'useragents': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['themes']