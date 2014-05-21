# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models
from misago.conf.migrationutils import migrate_settings_group, with_conf_models
from misago.core.migrationutils import ugettext_lazy as _


class Migration(SchemaMigration):
    def forwards(self, orm):
        migrate_settings_group(
            orm,
            {
                'key': 'users',
                'name': _("Users"),
                'settings': (
                    {
                        'setting': 'account_activation',
                        'name': _("New accounts activation"),
                        'legend': _("New accounts"),
                        'value': 'none',
                        'form_field': 'select',
                        'field_extra': {
                            'choices': (
                                ('none', _("No activation required")),
                                ('user', _("Activation Token sent to User")),
                                ('admin', _("Activation by Administrator")),
                                ('block', _("Don't allow new registrations"))
                            )
                        },
                    },
                    {
                        'setting': 'default_timezone',
                        'name': _("Default timezone"),
                        'description': _("Default timezone for newly "
                                         "registered accouts as well as "
                                         "unsigned users."),
                        'value': 'utc',
                        'form_field': 'select',
                        'field_extra': {
                            'choices': '#TZ#',
                        },
                    },
                    {
                        'setting': 'username_length_min',
                        'name': _("Minimal allowed username length"),
                        'legend': _("User names"),
                        'python_type': 'int',
                        'value': 3,
                        'field_extra': {
                            'min_value': 2,
                            'max_value': 255,
                        },
                    },
                    {
                        'setting': 'username_length_max',
                        'name': _("Maximal allowed username length"),
                        'python_type': 'int',
                        'value': 14,
                        'field_extra': {
                            'min_value': 2,
                            'max_value': 255,
                        },
                    },
                    {
                        'setting': 'password_length_min',
                        'name': _("Minimum user password length"),
                        'legend': _("Passwords"),
                        'python_type': 'int',
                        'value': 5,
                        'field_extra': {
                            'min_value': 2,
                            'max_value': 255,
                        },
                    },
                    {
                        'setting': 'avatars_types',
                        'name': _("Available avatar types"),
                        'legend': _("Avatars"),
                        'python_type': 'list',
                        'value': ['gravatar', 'upload'],
                        'form_field': 'checkbox',
                        'field_extra': {
                            'choices': (
                                ('gravatar', _("Gravatar")),
                                ('upload', _("Uploaded avatar")),
                                ('gallery', _("Avatars gallery"))
                            ),
                            'min': 1,
                        },
                    },
                    {
                        'setting': 'default_avatar',
                        'name': _("Default avatar"),
                        'value': 'gravatar',
                        'form_field': 'select',
                        'field_extra': {
                            'choices': (
                                ('gravatar', _("Gravatar")),
                                ('gallery', _("Random avatar from gallery")),
                            ),
                        },
                    },
                    {
                        'setting': 'avatar_upload_limit',
                        'name': _("Maximum size of uploaded avatar"),
                        'description': _("Enter maximum allowed file size "
                                         "(in KB) for avatar uploads"),
                        'python_type': 'int',
                        'value': 128,
                        'field_extra': {
                            'min_value': 0,
                        },
                    },
                    {
                        'setting': 'subscribe_start',
                        'name': _("Subscribe to started threads"),
                        'legend': _("Default subscriptions settings"),
                        'value': 'watch_email',
                        'form_field': 'select',
                        'field_extra': {
                            'choices': (
                                ('no', _("Don't watch")),
                                ('', _("Put on watched threads list")),
                                ('watch_email', _("Put on watched threads "
                                                  "list and e-mail user when "
                                                  "somebody replies")),
                            ),
                        },
                    },
                    {
                        'setting': 'subscribe_reply',
                        'name': _("Subscribe to replied threads"),
                        'value': 'watch_email',
                        'form_field': 'select',
                        'field_extra': {
                            'choices': (
                                ('no', _("Don't watch")),
                                ('', _("Put on watched threads list")),
                                ('watch_email', _("Put on watched threads "
                                                  "list and e-mail user when "
                                                  "somebody replies")),
                            ),
                        },
                    },
                )
            },
        )

    def backwards(self, orm):
        pass

    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'users.rank': {
            'Meta': {'object_name': 'Rank'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_default': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_on_index': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_tab': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'style': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'users.user': {
            'Meta': {'object_name': 'User'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '255', 'db_index': 'True'}),
            'email_hash': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'joined_on': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'rank': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['users.Rank']", 'on_delete': 'models.PROTECT'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'username_slug': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        }
    }

    complete_apps = ['users']

    depends_on = (
        ("conf", "0001_initial"),
    )

