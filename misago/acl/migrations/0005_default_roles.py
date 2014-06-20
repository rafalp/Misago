# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models
from misago.core.migrationutils import ugettext_lazy as _


class Migration(DataMigration):

    def forwards(self, orm):
        "Write your forwards methods here."
        orm.Role.objects.create(name=_('Guest').message,
                                special_role='anonymous')

        orm.Role.objects.create(name=_('Member').message,
                                special_role='member')

        # Note: Don't use "from appname.models import ModelName".
        # Use orm.ModelName to refer to models in this application,
        # and orm['appname.ModelName'] for models in other applications.

    models = {
        u'acl.role': {
            'Meta': {'object_name': 'Role'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'pickled_permissions': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'special_role': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['acl']
    symmetrical = True
