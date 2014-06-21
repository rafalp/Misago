# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('misago_acl', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Forum',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('special_role', models.CharField(max_length=255, null=True, blank=True)),
                ('role', models.CharField(max_length=255, null=True, blank=True)),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField(max_length=255)),
                ('description', models.TextField(null=True, blank=True)),
                ('description_as_html', models.TextField(null=True, blank=True)),
                ('is_closed', models.BooleanField(default=False)),
                ('redirect_url', models.CharField(max_length=255, null=True, blank=True)),
                ('redirects_count', models.PositiveIntegerField(default=0)),
                ('threads', models.PositiveIntegerField(default=0)),
                ('threads_count', models.PositiveIntegerField(default=0)),
                ('posts', models.PositiveIntegerField(default=0)),
                ('posts_count', models.PositiveIntegerField(default=0)),
                ('prune_started_after', models.PositiveIntegerField(default=0)),
                ('prune_replied_after', models.PositiveIntegerField(default=0)),
                ('css_class', models.CharField(max_length=255, null=True, blank=True)),
                ('lft', models.PositiveIntegerField(editable=False, db_index=True)),
                ('rght', models.PositiveIntegerField(editable=False, db_index=True)),
                ('tree_id', models.PositiveIntegerField(editable=False, db_index=True)),
                ('level', models.PositiveIntegerField(editable=False, db_index=True)),
                ('archive_pruned_in', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to_field='id', blank=True, to='misago_forums.Forum', null=True)),
                ('parent', mptt.fields.TreeForeignKey(to_field='id', blank=True, to='misago_forums.Forum', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ForumRole',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('special_role', models.CharField(max_length=255, null=True, blank=True)),
                ('pickled_permissions', models.TextField(null=True, blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RoleForumACL',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('forum', models.ForeignKey(to='misago_forums.Forum', to_field='id')),
                ('forum_role', models.ForeignKey(to='misago_forums.ForumRole', to_field='id')),
                ('role', models.ForeignKey(to='misago_acl.Role', to_field='id')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
