# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Checkpoint.old_forum'
        db.add_column(u'misago_checkpoint', 'old_forum',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='+', null=True, to=orm['misago.Forum']),
                      keep_default=False)

        # Adding field 'Checkpoint.old_forum_name'
        db.add_column(u'misago_checkpoint', 'old_forum_name',
                      self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Checkpoint.old_forum_slug'
        db.add_column(u'misago_checkpoint', 'old_forum_slug',
                      self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Checkpoint.old_forum'
        db.delete_column(u'misago_checkpoint', 'old_forum_id')

        # Deleting field 'Checkpoint.old_forum_name'
        db.delete_column(u'misago_checkpoint', 'old_forum_name')

        # Deleting field 'Checkpoint.old_forum_slug'
        db.delete_column(u'misago_checkpoint', 'old_forum_slug')


    models = {
        'misago.alert': {
            'Meta': {'object_name': 'Alert'},
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['misago.User']"}),
            'variables': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        'misago.ban': {
            'Meta': {'object_name': 'Ban'},
            'ban': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'expires': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'reason_admin': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'reason_user': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'test': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        },
        'misago.change': {
            'Meta': {'object_name': 'Change'},
            'agent': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'change': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            'forum': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['misago.Forum']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.GenericIPAddressField', [], {'max_length': '39'}),
            'post': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['misago.Post']"}),
            'post_content': ('django.db.models.fields.TextField', [], {}),
            'reason': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'size': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'thread': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['misago.Thread']"}),
            'thread_name_new': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'thread_name_old': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['misago.User']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'user_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'user_slug': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'misago.checkpoint': {
            'Meta': {'object_name': 'Checkpoint'},
            'action': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'agent': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            'forum': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['misago.Forum']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.GenericIPAddressField', [], {'max_length': '39'}),
            'old_forum': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': "orm['misago.Forum']"}),
            'old_forum_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'old_forum_slug': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'post': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['misago.Post']"}),
            'target_user': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['misago.User']"}),
            'target_user_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'target_user_slug': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'thread': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['misago.Thread']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['misago.User']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'user_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'user_slug': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'misago.fixture': {
            'Meta': {'object_name': 'Fixture'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'misago.forum': {
            'Meta': {'object_name': 'Forum'},
            'attrs': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'closed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description_preparsed': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_poster': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['misago.User']"}),
            'last_poster_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'last_poster_slug': ('django.db.models.fields.SlugField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'last_poster_style': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'last_thread': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['misago.Thread']"}),
            'last_thread_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'last_thread_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'last_thread_slug': ('django.db.models.fields.SlugField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': "orm['misago.Forum']"}),
            'posts': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'posts_delta': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'prune_last': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'prune_start': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'redirect': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'redirects': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'redirects_delta': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'show_details': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255'}),
            'special': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'style': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'threads': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'threads_delta': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '12'})
        },
        'misago.forumread': {
            'Meta': {'object_name': 'ForumRead'},
            'cleared': ('django.db.models.fields.DateTimeField', [], {}),
            'forum': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['misago.Forum']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['misago.User']"})
        },
        'misago.forumrole': {
            'Meta': {'object_name': 'ForumRole'},
            '_permissions': ('django.db.models.fields.TextField', [], {'null': 'True', 'db_column': "'permissions'", 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'misago.karma': {
            'Meta': {'object_name': 'Karma'},
            'agent': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            'forum': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['misago.Forum']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.GenericIPAddressField', [], {'max_length': '39'}),
            'post': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['misago.Post']"}),
            'score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'thread': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['misago.Thread']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['misago.User']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'user_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'user_slug': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'misago.monitoritem': {
            'Meta': {'object_name': 'MonitorItem'},
            'id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'primary_key': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'value': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        'misago.newsletter': {
            'Meta': {'object_name': 'Newsletter'},
            'content_html': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'content_plain': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ignore_subscriptions': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'progress': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'ranks': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['misago.Rank']", 'symmetrical': 'False'}),
            'step_size': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'token': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        },
        'misago.post': {
            'Meta': {'object_name': 'Post'},
            'agent': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'checkpoints': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'downvotes': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'edit_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'edit_reason': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'edit_user': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['misago.User']"}),
            'edit_user_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'edit_user_slug': ('django.db.models.fields.SlugField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'edits': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'forum': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['misago.Forum']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.GenericIPAddressField', [], {'max_length': '39'}),
            'mentions': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'mention_set'", 'symmetrical': 'False', 'to': "orm['misago.User']"}),
            'merge': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'moderated': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'post': ('django.db.models.fields.TextField', [], {}),
            'post_preparsed': ('django.db.models.fields.TextField', [], {}),
            'protected': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'reported': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'thread': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['misago.Thread']"}),
            'upvotes': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['misago.User']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'user_name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'misago.pruningpolicy': {
            'Meta': {'object_name': 'PruningPolicy'},
            'email': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_visit': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'posts': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'registered': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        },
        'misago.rank': {
            'Meta': {'object_name': 'Rank'},
            'as_tab': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'criteria': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'on_index': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'special': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'style': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'misago.role': {
            'Meta': {'object_name': 'Role'},
            '_permissions': ('django.db.models.fields.TextField', [], {'null': 'True', 'db_column': "'permissions'", 'blank': 'True'}),
            '_special': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'special'", 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'protected': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'misago.session': {
            'Meta': {'object_name': 'Session'},
            'admin': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'agent': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'crawler': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'data': ('django.db.models.fields.TextField', [], {'db_column': "'session_data'"}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '42', 'primary_key': 'True'}),
            'ip': ('django.db.models.fields.GenericIPAddressField', [], {'max_length': '39'}),
            'last': ('django.db.models.fields.DateTimeField', [], {}),
            'matched': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'rank': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sessions'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['misago.Rank']"}),
            'start': ('django.db.models.fields.DateTimeField', [], {}),
            'team': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sessions'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['misago.User']"})
        },
        'misago.setting': {
            'Meta': {'object_name': 'Setting'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'extra': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'field': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['misago.SettingsGroup']", 'to_field': "'key'"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'normalize_to': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'position': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'separator': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'setting': ('django.db.models.fields.CharField', [], {'max_length': '255', 'primary_key': 'True'}),
            'value': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'value_default': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        'misago.settingsgroup': {
            'Meta': {'object_name': 'SettingsGroup'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'misago.signinattempt': {
            'Meta': {'object_name': 'SignInAttempt'},
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.GenericIPAddressField', [], {'max_length': '39'})
        },
        'misago.themeadjustment': {
            'Meta': {'object_name': 'ThemeAdjustment'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'theme': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'useragents': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        'misago.thread': {
            'Meta': {'object_name': 'Thread'},
            'closed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'downvotes': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'forum': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['misago.Forum']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last': ('django.db.models.fields.DateTimeField', [], {}),
            'last_post': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['misago.Post']"}),
            'last_poster': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['misago.User']"}),
            'last_poster_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'last_poster_slug': ('django.db.models.fields.SlugField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'last_poster_style': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'merges': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'moderated': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'participants': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'private_thread_set'", 'symmetrical': 'False', 'to': "orm['misago.User']"}),
            'replies': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'replies_deleted': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'replies_moderated': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'replies_reported': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'score': ('django.db.models.fields.PositiveIntegerField', [], {'default': '30'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255'}),
            'start': ('django.db.models.fields.DateTimeField', [], {}),
            'start_post': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['misago.Post']"}),
            'start_poster': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['misago.User']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'start_poster_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'start_poster_slug': ('django.db.models.fields.SlugField', [], {'max_length': '255'}),
            'start_poster_style': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'upvotes': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'weight': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        },
        'misago.threadread': {
            'Meta': {'object_name': 'ThreadRead'},
            'forum': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['misago.Forum']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'thread': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['misago.Thread']"}),
            'updated': ('django.db.models.fields.DateTimeField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['misago.User']"})
        },
        'misago.token': {
            'Meta': {'object_name': 'Token'},
            'accessed': ('django.db.models.fields.DateTimeField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '42', 'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'signin_tokens'", 'to': "orm['misago.User']"})
        },
        'misago.user': {
            'Meta': {'object_name': 'User'},
            'acl_key': ('django.db.models.fields.CharField', [], {'max_length': '12', 'null': 'True', 'blank': 'True'}),
            'activation': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'alerts': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'alerts_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'allow_pds': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'avatar_ban': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'avatar_ban_reason_admin': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'avatar_ban_reason_user': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'avatar_image': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'avatar_original': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'avatar_temp': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'avatar_type': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '255'}),
            'email_hash': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32'}),
            'followers': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'following': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'follows': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'follows_set'", 'symmetrical': 'False', 'to': "orm['misago.User']"}),
            'hide_activity': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ignores': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'ignores_set'", 'symmetrical': 'False', 'to': "orm['misago.User']"}),
            'is_team': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'join_agent': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'join_date': ('django.db.models.fields.DateTimeField', [], {}),
            'join_ip': ('django.db.models.fields.GenericIPAddressField', [], {'max_length': '39'}),
            'karma_given_n': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'karma_given_p': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'karma_n': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'karma_p': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'last_agent': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'last_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'last_ip': ('django.db.models.fields.GenericIPAddressField', [], {'max_length': '39', 'null': 'True', 'blank': 'True'}),
            'last_post': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'last_search': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'last_sync': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'password_date': ('django.db.models.fields.DateTimeField', [], {}),
            'posts': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'rank': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['misago.Rank']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'ranking': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'receive_newsletters': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'roles': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['misago.Role']", 'symmetrical': 'False'}),
            'score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'signature': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'signature_ban': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'signature_ban_reason_admin': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'signature_ban_reason_user': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'signature_preparsed': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'subscribe_reply': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'subscribe_start': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'sync_pds': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'threads': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'timezone': ('django.db.models.fields.CharField', [], {'default': "'utc'", 'max_length': '255'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'token': ('django.db.models.fields.CharField', [], {'max_length': '12', 'null': 'True', 'blank': 'True'}),
            'unread_pds': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'username_slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255'}),
            'votes': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        },
        'misago.usernamechange': {
            'Meta': {'object_name': 'UsernameChange'},
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'old_username': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'namechanges'", 'to': "orm['misago.User']"})
        },
        'misago.watchedthread': {
            'Meta': {'object_name': 'WatchedThread'},
            'email': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'forum': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['misago.Forum']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_read': ('django.db.models.fields.DateTimeField', [], {}),
            'thread': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['misago.Thread']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['misago.User']"})
        }
    }

    complete_apps = ['misago']