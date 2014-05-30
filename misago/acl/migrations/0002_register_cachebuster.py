# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models
from misago.core.migrationutils import (with_core_models,
                                        cachebuster_register_cache)


class Migration(DataMigration):

    def forwards(self, orm):
        cachebuster_register_cache(orm, 'misago_acl')

    def backwards(self, orm):
        pass

    models = with_core_models('0001_initial', {
        u'acl.forumrole': {
            'Meta': {'object_name': 'ForumRole'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'pickled_permissions': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        u'acl.role': {
            'Meta': {'object_name': 'Role'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'pickled_permissions': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        }
    })

    complete_apps = ['acl', 'core']

    symmetrical = True

    depends_on = (
        ("core", "0001_initial"),
    )
