# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Alert'
        db.create_table(u'misago_alert', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['misago.User'])),
            ('date', self.gf('django.db.models.fields.DateTimeField')()),
            ('message', self.gf('django.db.models.fields.TextField')()),
            ('variables', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('misago', ['Alert'])

        # Adding model 'Ban'
        db.create_table(u'misago_ban', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('test', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('ban', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('reason_user', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('reason_admin', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('expires', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal('misago', ['Ban'])

        # Adding model 'Change'
        db.create_table(u'misago_change', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('forum', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['misago.Forum'])),
            ('thread', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['misago.Thread'])),
            ('post', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['misago.Post'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['misago.User'], null=True, on_delete=models.SET_NULL, blank=True)),
            ('user_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('user_slug', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('date', self.gf('django.db.models.fields.DateTimeField')()),
            ('ip', self.gf('django.db.models.fields.GenericIPAddressField')(max_length=39)),
            ('agent', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('reason', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('thread_name_new', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('thread_name_old', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('post_content', self.gf('django.db.models.fields.TextField')()),
            ('size', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('change', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('misago', ['Change'])

        # Adding model 'Checkpoint'
        db.create_table(u'misago_checkpoint', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('forum', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['misago.Forum'])),
            ('thread', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['misago.Thread'])),
            ('post', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['misago.Post'])),
            ('action', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['misago.User'], null=True, on_delete=models.SET_NULL, blank=True)),
            ('user_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('user_slug', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('target_user', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='+', null=True, on_delete=models.SET_NULL, to=orm['misago.User'])),
            ('target_user_name', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('target_user_slug', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('date', self.gf('django.db.models.fields.DateTimeField')()),
            ('ip', self.gf('django.db.models.fields.GenericIPAddressField')(max_length=39)),
            ('agent', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('misago', ['Checkpoint'])

        # Adding model 'Fixture'
        db.create_table(u'misago_fixture', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('misago', ['Fixture'])

        # Adding model 'Forum'
        db.create_table(u'misago_forum', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('parent', self.gf('mptt.fields.TreeForeignKey')(blank=True, related_name='children', null=True, to=orm['misago.Forum'])),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=12)),
            ('special', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('description_preparsed', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('threads', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('threads_delta', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('posts', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('posts_delta', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('redirects', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('redirects_delta', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('last_thread', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='+', null=True, on_delete=models.SET_NULL, to=orm['misago.Thread'])),
            ('last_thread_name', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('last_thread_slug', self.gf('django.db.models.fields.SlugField')(max_length=255, null=True, blank=True)),
            ('last_thread_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('last_poster', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='+', null=True, on_delete=models.SET_NULL, to=orm['misago.User'])),
            ('last_poster_name', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('last_poster_slug', self.gf('django.db.models.fields.SlugField')(max_length=255, null=True, blank=True)),
            ('last_poster_style', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('prune_start', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('prune_last', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('redirect', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('attrs', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('show_details', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('style', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('closed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('lft', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('rght', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('tree_id', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('level', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
        ))
        db.send_create_signal('misago', ['Forum'])

        # Adding model 'ForumRead'
        db.create_table(u'misago_forumread', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['misago.User'])),
            ('forum', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['misago.Forum'])),
            ('updated', self.gf('django.db.models.fields.DateTimeField')()),
            ('cleared', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('misago', ['ForumRead'])

        # Adding model 'ForumRole'
        db.create_table(u'misago_forumrole', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('_permissions', self.gf('django.db.models.fields.TextField')(null=True, db_column='permissions', blank=True)),
        ))
        db.send_create_signal('misago', ['ForumRole'])

        # Adding model 'Karma'
        db.create_table(u'misago_karma', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('forum', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['misago.Forum'])),
            ('thread', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['misago.Thread'])),
            ('post', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['misago.Post'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['misago.User'], null=True, on_delete=models.SET_NULL, blank=True)),
            ('user_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('user_slug', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('date', self.gf('django.db.models.fields.DateTimeField')()),
            ('ip', self.gf('django.db.models.fields.GenericIPAddressField')(max_length=39)),
            ('agent', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('score', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('misago', ['Karma'])

        # Adding model 'MonitorItem'
        db.create_table(u'misago_monitoritem', (
            ('id', self.gf('django.db.models.fields.CharField')(max_length=255, primary_key=True)),
            ('value', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal('misago', ['MonitorItem'])

        # Adding model 'Newsletter'
        db.create_table(u'misago_newsletter', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('token', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('step_size', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('progress', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('content_html', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('content_plain', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('ignore_subscriptions', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('misago', ['Newsletter'])

        # Adding M2M table for field ranks on 'Newsletter'
        db.create_table(u'misago_newsletter_ranks', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('newsletter', models.ForeignKey(orm['misago.newsletter'], null=False)),
            ('rank', models.ForeignKey(orm['misago.rank'], null=False))
        ))
        db.create_unique(u'misago_newsletter_ranks', ['newsletter_id', 'rank_id'])

        # Adding model 'Post'
        db.create_table(u'misago_post', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('forum', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['misago.Forum'])),
            ('thread', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['misago.Thread'])),
            ('merge', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['misago.User'], null=True, on_delete=models.SET_NULL, blank=True)),
            ('user_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('ip', self.gf('django.db.models.fields.GenericIPAddressField')(max_length=39)),
            ('agent', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('post', self.gf('django.db.models.fields.TextField')()),
            ('post_preparsed', self.gf('django.db.models.fields.TextField')()),
            ('upvotes', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('downvotes', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('checkpoints', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('date', self.gf('django.db.models.fields.DateTimeField')()),
            ('edits', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('edit_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('edit_reason', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('edit_user', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='+', null=True, on_delete=models.SET_NULL, to=orm['misago.User'])),
            ('edit_user_name', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('edit_user_slug', self.gf('django.db.models.fields.SlugField')(max_length=255, null=True, blank=True)),
            ('reported', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('moderated', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('protected', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('misago', ['Post'])

        # Adding M2M table for field mentions on 'Post'
        db.create_table(u'misago_post_mentions', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('post', models.ForeignKey(orm['misago.post'], null=False)),
            ('user', models.ForeignKey(orm['misago.user'], null=False))
        ))
        db.create_unique(u'misago_post_mentions', ['post_id', 'user_id'])

        # Adding model 'PruningPolicy'
        db.create_table(u'misago_pruningpolicy', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('email', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('posts', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('registered', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('last_visit', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
        ))
        db.send_create_signal('misago', ['PruningPolicy'])

        # Adding model 'Rank'
        db.create_table(u'misago_rank', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('slug', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('style', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('special', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('as_tab', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('on_index', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('order', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('criteria', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal('misago', ['Rank'])

        # Adding model 'Role'
        db.create_table(u'misago_role', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('_special', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='special', blank=True)),
            ('protected', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('_permissions', self.gf('django.db.models.fields.TextField')(null=True, db_column='permissions', blank=True)),
        ))
        db.send_create_signal('misago', ['Role'])

        # Adding model 'Session'
        db.create_table(u'misago_session', (
            ('id', self.gf('django.db.models.fields.CharField')(max_length=42, primary_key=True)),
            ('data', self.gf('django.db.models.fields.TextField')(db_column='session_data')),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='sessions', null=True, on_delete=models.SET_NULL, to=orm['misago.User'])),
            ('crawler', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('ip', self.gf('django.db.models.fields.GenericIPAddressField')(max_length=39)),
            ('agent', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('start', self.gf('django.db.models.fields.DateTimeField')()),
            ('last', self.gf('django.db.models.fields.DateTimeField')()),
            ('team', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('rank', self.gf('django.db.models.fields.related.ForeignKey')(related_name='sessions', null=True, on_delete=models.SET_NULL, to=orm['misago.Rank'])),
            ('admin', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('matched', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('hidden', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('misago', ['Session'])

        # Adding model 'Setting'
        db.create_table(u'misago_setting', (
            ('setting', self.gf('django.db.models.fields.CharField')(max_length=255, primary_key=True)),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['misago.SettingsGroup'], to_field='key')),
            ('value', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('value_default', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('normalize_to', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('field', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('extra', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('position', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('separator', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('misago', ['Setting'])

        # Adding model 'SettingsGroup'
        db.create_table(u'misago_settingsgroup', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('key', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('misago', ['SettingsGroup'])

        # Adding model 'SignInAttempt'
        db.create_table(u'misago_signinattempt', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ip', self.gf('django.db.models.fields.GenericIPAddressField')(max_length=39)),
            ('date', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('misago', ['SignInAttempt'])

        # Adding model 'ThemeAdjustment'
        db.create_table(u'misago_themeadjustment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('theme', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('useragents', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('misago', ['ThemeAdjustment'])

        # Adding model 'Thread'
        db.create_table(u'misago_thread', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('forum', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['misago.Forum'])),
            ('weight', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=255)),
            ('replies', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('replies_reported', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('replies_moderated', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('replies_deleted', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('merges', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('score', self.gf('django.db.models.fields.PositiveIntegerField')(default=30)),
            ('upvotes', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('downvotes', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('start', self.gf('django.db.models.fields.DateTimeField')()),
            ('start_post', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='+', null=True, on_delete=models.SET_NULL, to=orm['misago.Post'])),
            ('start_poster', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['misago.User'], null=True, on_delete=models.SET_NULL, blank=True)),
            ('start_poster_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('start_poster_slug', self.gf('django.db.models.fields.SlugField')(max_length=255)),
            ('start_poster_style', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('last', self.gf('django.db.models.fields.DateTimeField')()),
            ('last_post', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='+', null=True, on_delete=models.SET_NULL, to=orm['misago.Post'])),
            ('last_poster', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='+', null=True, on_delete=models.SET_NULL, to=orm['misago.User'])),
            ('last_poster_name', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('last_poster_slug', self.gf('django.db.models.fields.SlugField')(max_length=255, null=True, blank=True)),
            ('last_poster_style', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('moderated', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('closed', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('misago', ['Thread'])

        # Adding M2M table for field participants on 'Thread'
        db.create_table(u'misago_thread_participants', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('thread', models.ForeignKey(orm['misago.thread'], null=False)),
            ('user', models.ForeignKey(orm['misago.user'], null=False))
        ))
        db.create_unique(u'misago_thread_participants', ['thread_id', 'user_id'])

        # Adding model 'ThreadRead'
        db.create_table(u'misago_threadread', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['misago.User'])),
            ('forum', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['misago.Forum'])),
            ('thread', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['misago.Thread'])),
            ('updated', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('misago', ['ThreadRead'])

        # Adding model 'Token'
        db.create_table(u'misago_token', (
            ('id', self.gf('django.db.models.fields.CharField')(max_length=42, primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='signin_tokens', to=orm['misago.User'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')()),
            ('accessed', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('misago', ['Token'])

        # Adding model 'User'
        db.create_table(u'misago_user', (
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
            ('rank', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['misago.Rank'], null=True, on_delete=models.SET_NULL, blank=True)),
            ('last_sync', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('last_post', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('last_search', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('alerts', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('alerts_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('unread_pds', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
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
        db.send_create_signal('misago', ['User'])

        # Adding M2M table for field follows on 'User'
        db.create_table(u'misago_user_follows', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_user', models.ForeignKey(orm['misago.user'], null=False)),
            ('to_user', models.ForeignKey(orm['misago.user'], null=False))
        ))
        db.create_unique(u'misago_user_follows', ['from_user_id', 'to_user_id'])

        # Adding M2M table for field ignores on 'User'
        db.create_table(u'misago_user_ignores', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_user', models.ForeignKey(orm['misago.user'], null=False)),
            ('to_user', models.ForeignKey(orm['misago.user'], null=False))
        ))
        db.create_unique(u'misago_user_ignores', ['from_user_id', 'to_user_id'])

        # Adding M2M table for field roles on 'User'
        db.create_table(u'misago_user_roles', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('user', models.ForeignKey(orm['misago.user'], null=False)),
            ('role', models.ForeignKey(orm['misago.role'], null=False))
        ))
        db.create_unique(u'misago_user_roles', ['user_id', 'role_id'])

        # Adding model 'UsernameChange'
        db.create_table(u'misago_usernamechange', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='namechanges', to=orm['misago.User'])),
            ('date', self.gf('django.db.models.fields.DateTimeField')()),
            ('old_username', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('misago', ['UsernameChange'])

        # Adding model 'WatchedThread'
        db.create_table(u'misago_watchedthread', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['misago.User'])),
            ('forum', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['misago.Forum'])),
            ('thread', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['misago.Thread'])),
            ('last_read', self.gf('django.db.models.fields.DateTimeField')()),
            ('email', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('misago', ['WatchedThread'])


    def backwards(self, orm):
        # Deleting model 'Alert'
        db.delete_table(u'misago_alert')

        # Deleting model 'Ban'
        db.delete_table(u'misago_ban')

        # Deleting model 'Change'
        db.delete_table(u'misago_change')

        # Deleting model 'Checkpoint'
        db.delete_table(u'misago_checkpoint')

        # Deleting model 'Fixture'
        db.delete_table(u'misago_fixture')

        # Deleting model 'Forum'
        db.delete_table(u'misago_forum')

        # Deleting model 'ForumRead'
        db.delete_table(u'misago_forumread')

        # Deleting model 'ForumRole'
        db.delete_table(u'misago_forumrole')

        # Deleting model 'Karma'
        db.delete_table(u'misago_karma')

        # Deleting model 'MonitorItem'
        db.delete_table(u'misago_monitoritem')

        # Deleting model 'Newsletter'
        db.delete_table(u'misago_newsletter')

        # Removing M2M table for field ranks on 'Newsletter'
        db.delete_table('misago_newsletter_ranks')

        # Deleting model 'Post'
        db.delete_table(u'misago_post')

        # Removing M2M table for field mentions on 'Post'
        db.delete_table('misago_post_mentions')

        # Deleting model 'PruningPolicy'
        db.delete_table(u'misago_pruningpolicy')

        # Deleting model 'Rank'
        db.delete_table(u'misago_rank')

        # Deleting model 'Role'
        db.delete_table(u'misago_role')

        # Deleting model 'Session'
        db.delete_table(u'misago_session')

        # Deleting model 'Setting'
        db.delete_table(u'misago_setting')

        # Deleting model 'SettingsGroup'
        db.delete_table(u'misago_settingsgroup')

        # Deleting model 'SignInAttempt'
        db.delete_table(u'misago_signinattempt')

        # Deleting model 'ThemeAdjustment'
        db.delete_table(u'misago_themeadjustment')

        # Deleting model 'Thread'
        db.delete_table(u'misago_thread')

        # Removing M2M table for field participants on 'Thread'
        db.delete_table('misago_thread_participants')

        # Deleting model 'ThreadRead'
        db.delete_table(u'misago_threadread')

        # Deleting model 'Token'
        db.delete_table(u'misago_token')

        # Deleting model 'User'
        db.delete_table(u'misago_user')

        # Removing M2M table for field follows on 'User'
        db.delete_table('misago_user_follows')

        # Removing M2M table for field ignores on 'User'
        db.delete_table('misago_user_ignores')

        # Removing M2M table for field roles on 'User'
        db.delete_table('misago_user_roles')

        # Deleting model 'UsernameChange'
        db.delete_table(u'misago_usernamechange')

        # Deleting model 'WatchedThread'
        db.delete_table(u'misago_watchedthread')


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
            'hidden': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
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
            'participants': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'+'", 'symmetrical': 'False', 'to': "orm['misago.User']"}),
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