# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import django.db.models.deletion
from django.conf import settings

from misago.core.pgutils import CreatePartialIndex


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
        ('misago_acl', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login')),
                ('username', models.CharField(max_length=30)),
                ('username_slug', models.CharField(unique=True, max_length=30)),
                ('email', models.EmailField(max_length=255, db_index=True)),
                ('email_hash', models.CharField(unique=True, max_length=32)),
                ('joined_on', models.DateTimeField(default=django.utils.timezone.now, verbose_name='joined on')),
                ('joined_from_ip', models.GenericIPAddressField()),
                ('last_ip', models.GenericIPAddressField(null=True, blank=True)),
                ('presence_visibility', models.PositiveIntegerField(default=0)),
                ('timezone', models.CharField(max_length=255, default='utc')),
                ('title', models.CharField(max_length=255, null=True, blank=True)),
                ('requires_activation', models.PositiveIntegerField(default=0)),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into admin sites.', verbose_name='staff status')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('acl_key', models.CharField(max_length=12, null=True, blank=True)),
                ('groups', models.ManyToManyField(to='auth.Group', verbose_name='groups', blank=True)),
                ('roles', models.ManyToManyField(to='misago_acl.Role')),
                ('user_permissions', models.ManyToManyField(to='auth.Permission', verbose_name='user permissions', blank=True)),
                ('is_avatar_banned', models.BooleanField(default=False)),
                ('avatar_type', models.CharField(max_length=10, null=True, blank=True)),
                ('avatar_image', models.CharField(max_length=255, null=True, blank=True)),
                ('avatar_original', models.CharField(max_length=255, null=True, blank=True)),
                ('avatar_temp', models.CharField(max_length=255, null=True, blank=True)),
                ('avatar_crop', models.CharField(max_length=255, null=True, blank=True)),
                ('avatar_ban_user_message', models.TextField(null=True, blank=True)),
                ('avatar_ban_staff_message', models.TextField(null=True, blank=True)),
                ('is_signature_banned', models.BooleanField(default=False)),
                ('signature', models.TextField(null=True, blank=True)),
                ('signature_preparsed', models.TextField(null=True, blank=True)),
                ('signature_ban_user_message', models.TextField(null=True, blank=True)),
                ('signature_ban_staff_message', models.TextField(null=True, blank=True)),
                ('warning_level', models.PositiveIntegerField(default=0)),
                ('warning_level_update_on', models.DateTimeField(null=True, blank=True)),
                ('following', models.PositiveIntegerField(default=0)),
                ('followers', models.PositiveIntegerField(default=0)),
                ('new_alerts', models.PositiveIntegerField(default=0)),
                ('limit_private_thread_invites', models.PositiveIntegerField(default=0)),
                ('unread_private_threads', models.PositiveIntegerField(default=0)),
                ('sync_unred_private_threads', models.BooleanField(default=False)),
                ('subscribe_to_started_threads', models.PositiveIntegerField(default=0)),
                ('subscribe_to_replied_threads', models.PositiveIntegerField(default=0)),
                ('threads', models.PositiveIntegerField(default=0)),
                ('posts', models.PositiveIntegerField(default=0)),
                ('last_post', models.DateTimeField(null=True, blank=True)),
                ('last_search', models.DateTimeField(null=True, blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        CreatePartialIndex(
            field='User.is_staff',
            index_name='misago_users_user_is_staff_partial',
            condition='is_staff = TRUE',
        ),
        CreatePartialIndex(
            field='User.requires_activation',
            index_name='misago_users_user_requires_activation_partial',
            condition='requires_activation > 0',
        ),
        migrations.CreateModel(
            name='Online',
            fields=[
                ('current_ip', models.GenericIPAddressField()),
                ('last_click', models.DateTimeField(default=django.utils.timezone.now)),
                ('user', models.OneToOneField(primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Rank',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('slug', models.CharField(max_length=255)),
                ('description', models.TextField(null=True, blank=True)),
                ('title', models.CharField(max_length=255, null=True, blank=True)),
                ('css_class', models.CharField(max_length=255, null=True, blank=True)),
                ('is_default', models.BooleanField(default=False)),
                ('is_tab', models.BooleanField(default=False)),
                ('is_on_index', models.BooleanField(default=False)),
                ('order', models.IntegerField(default=0)),
                ('roles', models.ManyToManyField(to='misago_acl.Role', null=True, blank=True)),
            ],
            options={
                'get_latest_by': b'order',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='user',
            name='rank',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to_field='id', to='misago_users.Rank'),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='Ban',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('test', models.PositiveIntegerField(default=0, db_index=True)),
                ('banned_value', models.CharField(max_length=255, db_index=True)),
                ('user_message', models.TextField(null=True, blank=True)),
                ('staff_message', models.TextField(null=True, blank=True)),
                ('valid_until', models.DateField(null=True, blank=True, db_index=True)),
                ('is_valid', models.BooleanField(default=True, db_index=True)),
            ],
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BanCache',
            fields=[
                ('user_message', models.TextField(null=True, blank=True)),
                ('staff_message', models.TextField(null=True, blank=True)),
                ('bans_version', models.PositiveIntegerField(default=0)),
                ('valid_until', models.DateField(null=True, blank=True)),
                ('is_banned', models.BooleanField(default=False)),
                ('user', models.OneToOneField(primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='WarningLevel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(null=True, blank=True)),
                ('level', models.PositiveIntegerField(default=1, db_index=True)),
                ('length_in_minutes', models.PositiveIntegerField(default=0)),
                ('restricts_posting_replies', models.PositiveIntegerField(default=0)),
                ('restricts_posting_threads', models.PositiveIntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
