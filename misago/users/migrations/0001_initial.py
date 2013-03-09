# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'User'
        db.create_table(u'users_user', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('username', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('username_slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=255)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=255)),
            ('email_hash', self.gf('django.db.models.fields.CharField')(unique=True, max_length=32)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('password_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('avatar_type', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('avatar_image', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('avatar_original', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('avatar_temp', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('signature', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('signature_preparsed', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('join_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('join_ip', self.gf('django.db.models.fields.GenericIPAddressField')(max_length=39)),
            ('join_agent', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('last_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('last_ip', self.gf('django.db.models.fields.GenericIPAddressField')(max_length=39, null=True, blank=True)),
            ('last_agent', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('hide_activity', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('allow_pms', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('subscribe_start', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('subscribe_reply', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('receive_newsletters', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('threads', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('posts', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('votes', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('karma_given_p', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('karma_given_n', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('karma_p', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('karma_n', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('following', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('followers', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('score', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('ranking', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('rank', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ranks.Rank'], null=True, on_delete=models.SET_NULL, blank=True)),
            ('last_sync', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('last_post', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('last_search', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('alerts', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('alerts_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('activation', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('token', self.gf('django.db.models.fields.CharField')(max_length=12, null=True, blank=True)),
            ('avatar_ban', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('avatar_ban_reason_user', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('avatar_ban_reason_admin', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('signature_ban', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('signature_ban_reason_user', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('signature_ban_reason_admin', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('timezone', self.gf('django.db.models.fields.CharField')(default='utc', max_length=255)),
            ('is_team', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('acl_key', self.gf('django.db.models.fields.CharField')(max_length=12, null=True, blank=True)),
        ))
        db.send_create_signal(u'users', ['User'])

        # Adding M2M table for field follows on 'User'
        db.create_table(u'users_user_follows', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_user', models.ForeignKey(orm[u'users.user'], null=False)),
            ('to_user', models.ForeignKey(orm[u'users.user'], null=False))
        ))
        db.create_unique(u'users_user_follows', ['from_user_id', 'to_user_id'])

        # Adding M2M table for field ignores on 'User'
        db.create_table(u'users_user_ignores', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_user', models.ForeignKey(orm[u'users.user'], null=False)),
            ('to_user', models.ForeignKey(orm[u'users.user'], null=False))
        ))
        db.create_unique(u'users_user_ignores', ['from_user_id', 'to_user_id'])

        # Adding M2M table for field roles on 'User'
        db.create_table(u'users_user_roles', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('user', models.ForeignKey(orm[u'users.user'], null=False)),
            ('role', models.ForeignKey(orm[u'roles.role'], null=False))
        ))
        db.create_unique(u'users_user_roles', ['user_id', 'role_id'])


    def backwards(self, orm):
        # Deleting model 'User'
        db.delete_table(u'users_user')

        # Removing M2M table for field follows on 'User'
        db.delete_table('users_user_follows')

        # Removing M2M table for field ignores on 'User'
        db.delete_table('users_user_ignores')

        # Removing M2M table for field roles on 'User'
        db.delete_table('users_user_roles')


    models = {
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
        },
        u'roles.role': {
            'Meta': {'object_name': 'Role'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'permissions': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'protected': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'token': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        u'users.user': {
            'Meta': {'object_name': 'User'},
            'acl_key': ('django.db.models.fields.CharField', [], {'max_length': '12', 'null': 'True', 'blank': 'True'}),
            'activation': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'alerts': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'alerts_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'allow_pms': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
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
            'follows': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'follows_set'", 'symmetrical': 'False', 'to': u"orm['users.User']"}),
            'hide_activity': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ignores': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'ignores_set'", 'symmetrical': 'False', 'to': u"orm['users.User']"}),
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
            'rank': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ranks.Rank']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'ranking': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'receive_newsletters': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'roles': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['roles.Role']", 'symmetrical': 'False'}),
            'score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'signature': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'signature_ban': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'signature_ban_reason_admin': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'signature_ban_reason_user': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'signature_preparsed': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'subscribe_reply': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'subscribe_start': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'threads': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'timezone': ('django.db.models.fields.CharField', [], {'default': "'utc'", 'max_length': '255'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'token': ('django.db.models.fields.CharField', [], {'max_length': '12', 'null': 'True', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'username_slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255'}),
            'votes': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['users']