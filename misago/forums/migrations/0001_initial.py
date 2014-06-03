# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Forum'
        db.create_table(u'forums_forum', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('parent', self.gf('mptt.fields.TreeForeignKey')(blank=True, related_name='children', null=True, to=orm['forums.Forum'])),
            ('special_role', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('role', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('description_preparsed', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('is_closed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('redirect_url', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('redirects_count', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('threads', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('threads_count', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('posts', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('posts_count', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('prune_started_after', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('prune_replied_after', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('archive_pruned_in', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='pruned_archive', null=True, on_delete=models.SET_NULL, to=orm['forums.Forum'])),
            ('css_class', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            (u'lft', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            (u'rght', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            (u'tree_id', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            (u'level', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
        ))
        db.send_create_signal(u'forums', ['Forum'])


    def backwards(self, orm):
        # Deleting model 'Forum'
        db.delete_table(u'forums_forum')


    models = {
        u'forums.forum': {
            'Meta': {'object_name': 'Forum'},
            'archive_pruned_in': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'pruned_archive'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['forums.Forum']"}),
            'css_class': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description_preparsed': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_closed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': u"orm['forums.Forum']"}),
            'posts': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'posts_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'prune_replied_after': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'prune_started_after': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'redirect_url': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'redirects_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            u'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'role': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255'}),
            'special_role': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'threads': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'threads_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            u'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        }
    }

    complete_apps = ['forums']