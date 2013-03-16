# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'SignInAttempt'
        db.create_table(u'bruteforce_signinattempt', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ip', self.gf('django.db.models.fields.GenericIPAddressField')(max_length=39)),
            ('date', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'bruteforce', ['SignInAttempt'])


    def backwards(self, orm):
        # Deleting model 'SignInAttempt'
        db.delete_table(u'bruteforce_signinattempt')


    models = {
        u'bruteforce.signinattempt': {
            'Meta': {'object_name': 'SignInAttempt'},
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.GenericIPAddressField', [], {'max_length': '39'})
        }
    }

    complete_apps = ['bruteforce']