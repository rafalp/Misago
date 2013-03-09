# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Newsletter'
        db.create_table(u'newsletters_newsletter', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('token', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('step_size', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('progress', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('content_html', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('content_plain', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('ignore_subscriptions', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'newsletters', ['Newsletter'])

        # Adding M2M table for field ranks on 'Newsletter'
        db.create_table(u'newsletters_newsletter_ranks', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('newsletter', models.ForeignKey(orm[u'newsletters.newsletter'], null=False)),
            ('rank', models.ForeignKey(orm[u'ranks.rank'], null=False))
        ))
        db.create_unique(u'newsletters_newsletter_ranks', ['newsletter_id', 'rank_id'])


    def backwards(self, orm):
        # Deleting model 'Newsletter'
        db.delete_table(u'newsletters_newsletter')

        # Removing M2M table for field ranks on 'Newsletter'
        db.delete_table('newsletters_newsletter_ranks')


    models = {
        u'newsletters.newsletter': {
            'Meta': {'object_name': 'Newsletter'},
            'content_html': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'content_plain': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ignore_subscriptions': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'progress': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'ranks': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['ranks.Rank']", 'symmetrical': 'False'}),
            'step_size': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'token': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        },
        u'ranks.rank': {
            'Meta': {'object_name': 'Rank'},
            'as_tab': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'criteria': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'name_slug': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'on_index': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'special': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'style': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['newsletters']