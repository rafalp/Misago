# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.db import migrations, models

import misago.users.avatars.store


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0001_initial'),
        ('misago_acl', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                (
                    'id', models.AutoField(
                        verbose_name='ID', serialize=False, auto_created=True, primary_key=True
                    )
                ),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                (
                    'last_login',
                    models.DateTimeField(null=True, blank=True, verbose_name='last login')
                ),
                ('username', models.CharField(max_length=30)),
                ('slug', models.CharField(unique=True, max_length=30)),
                ('email', models.EmailField(max_length=255, db_index=True)),
                ('email_hash', models.CharField(unique=True, max_length=32)),
                (
                    'joined_on', models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name='joined on'
                    )
                ),
                ('joined_from_ip', models.GenericIPAddressField()),
                ('last_ip', models.GenericIPAddressField(null=True, blank=True)),
                ('is_hiding_presence', models.BooleanField(default=False)),
                ('title', models.CharField(max_length=255, null=True, blank=True)),
                ('requires_activation', models.PositiveIntegerField(default=0)),
                (
                    'is_staff', models.BooleanField(
                        default=False,
                        help_text='Designates whether the user can log into admin sites.',
                        verbose_name='staff status'
                    )
                ),
                (
                    'is_superuser', models.BooleanField(
                        default=False,
                        help_text='Designates that this user has all permissions without explicitly assigning them.',
                        verbose_name='superuser status'
                    )
                ),
                ('acl_key', models.CharField(max_length=12, null=True, blank=True)),
                (
                    'is_active', models.BooleanField(
                        db_index=True,
                        default=True,
                        verbose_name='active',
                        help_text=(
                            'Designates whether this user should be treated as active. Unselect this instead of deleting '
                            'accounts.'
                        )
                    )
                ),
                ('is_active_staff_message', models.TextField(null=True, blank=True)),
                (
                    'groups', models.ManyToManyField(
                        related_query_name='user',
                        related_name='user_set',
                        to='auth.Group',
                        blank=True,
                        help_text='The groups this user belongs to. A user will get all permissions granted to each of his/her group.',
                        verbose_name='groups'
                    )
                ),
                ('roles', models.ManyToManyField(to='misago_acl.Role')),
                (
                    'user_permissions', models.ManyToManyField(
                        related_query_name='user',
                        related_name='user_set',
                        to='auth.Permission',
                        blank=True,
                        help_text='Specific permissions for this user.',
                        verbose_name='user permissions'
                    )
                ),
                (
                    'avatar_tmp', models.ImageField(
                        max_length=255,
                        upload_to=misago.users.avatars.store.upload_to,
                        null=True,
                        blank=True
                    )
                ),
                (
                    'avatar_src', models.ImageField(
                        max_length=255,
                        upload_to=misago.users.avatars.store.upload_to,
                        null=True,
                        blank=True
                    )
                ),
                ('avatar_crop', models.CharField(max_length=255, null=True, blank=True)),
                ('avatars', JSONField(null=True, blank=True)),
                ('is_avatar_locked', models.BooleanField(default=False)),
                ('avatar_lock_user_message', models.TextField(null=True, blank=True)),
                ('avatar_lock_staff_message', models.TextField(null=True, blank=True)),
                ('signature', models.TextField(null=True, blank=True)),
                ('signature_parsed', models.TextField(null=True, blank=True)),
                ('signature_checksum', models.CharField(max_length=64, null=True, blank=True)),
                ('is_signature_locked', models.BooleanField(default=False)),
                ('signature_lock_user_message', models.TextField(null=True, blank=True)),
                ('signature_lock_staff_message', models.TextField(null=True, blank=True)),
                ('following', models.PositiveIntegerField(default=0)),
                ('followers', models.PositiveIntegerField(default=0)),
                ('limits_private_thread_invites_to', models.PositiveIntegerField(default=0)),
                ('unread_private_threads', models.PositiveIntegerField(default=0)),
                ('sync_unread_private_threads', models.BooleanField(default=False)),
                ('subscribe_to_started_threads', models.PositiveIntegerField(default=0)),
                ('subscribe_to_replied_threads', models.PositiveIntegerField(default=0)),
                ('threads', models.PositiveIntegerField(default=0)),
                ('posts', models.PositiveIntegerField(default=0, db_index=True)),
                ('last_posted_on', models.DateTimeField(null=True, blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model, ),
        ),
        migrations.CreateModel(
            name='Online',
            fields=[
                ('current_ip', models.GenericIPAddressField()),
                ('last_click', models.DateTimeField(default=django.utils.timezone.now)),
                (
                    'user', models.OneToOneField(
                        related_name='online_tracker',
                        on_delete=django.db.models.deletion.CASCADE,
                        primary_key=True,
                        serialize=False,
                        to=settings.AUTH_USER_MODEL
                    )
                ),
            ],
            options={},
            bases=(models.Model, ),
        ),
        migrations.CreateModel(
            name='UsernameChange',
            fields=[
                (
                    'id', models.AutoField(
                        verbose_name='ID', serialize=False, auto_created=True, primary_key=True
                    )
                ),
                ('changed_by_username', models.CharField(max_length=30)),
                ('changed_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('new_username', models.CharField(max_length=255)),
                ('old_username', models.CharField(max_length=255)),
                (
                    'changed_by', models.ForeignKey(
                        related_name='user_renames',
                        on_delete=django.db.models.deletion.SET_NULL,
                        blank=True,
                        to=settings.AUTH_USER_MODEL,
                        null=True
                    )
                ),
                (
                    'user', models.ForeignKey(
                        related_name='namechanges',
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    )
                ),
            ],
            options={
                'get_latest_by': b'changed_on',
            },
            bases=(models.Model, ),
        ),
        migrations.CreateModel(
            name='Rank',
            fields=[
                (
                    'id', models.AutoField(
                        verbose_name='ID', serialize=False, auto_created=True, primary_key=True
                    )
                ),
                ('name', models.CharField(max_length=255)),
                ('slug', models.CharField(unique=True, max_length=255)),
                ('description', models.TextField(null=True, blank=True)),
                ('title', models.CharField(max_length=255, null=True, blank=True)),
                ('css_class', models.CharField(max_length=255, null=True, blank=True)),
                ('is_default', models.BooleanField(default=False)),
                ('is_tab', models.BooleanField(default=False)),
                ('order', models.IntegerField(default=0)),
                ('roles', models.ManyToManyField(to='misago_acl.Role', null=True, blank=True)),
            ],
            options={
                'get_latest_by': b'order',
            },
            bases=(models.Model, ),
        ),
        migrations.AddField(
            model_name='user',
            name='rank',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                to_field='id',
                blank=True,
                to='misago_users.Rank',
                null=True
            ),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='follows',
            field=models.ManyToManyField(related_name='followed_by', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='blocks',
            field=models.ManyToManyField(related_name='blocked_by', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='ActivityRanking',
            fields=[
                (
                    'id', models.AutoField(
                        verbose_name='ID', serialize=False, auto_created=True, primary_key=True
                    )
                ),
                (
                    'user', models.ForeignKey(
                        related_name='+',
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    )
                ),
                ('score', models.PositiveIntegerField(default=0, db_index=True)),
            ],
            options={},
            bases=(models.Model, ),
        ),
        migrations.CreateModel(
            name='Avatar',
            fields=[
                (
                    'id', models.AutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name='ID'
                    )
                ),
                (
                    'user', models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
                    )
                ),
                ('size', models.PositiveIntegerField(default=0)),
                (
                    'image', models.ImageField(
                        max_length=255, upload_to=misago.users.avatars.store.upload_to
                    )
                ),
            ],
        ),
        migrations.CreateModel(
            name='AvatarGallery',
            fields=[
                (
                    'id', models.AutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name='ID'
                    )
                ),
                ('gallery', models.CharField(max_length=255)),
                (
                    'image', models.ImageField(
                        max_length=255, upload_to=misago.users.avatars.store.upload_to
                    )
                ),
            ],
            options={
                'ordering': ['gallery', 'pk'],
            },
        ),
        migrations.CreateModel(
            name='Ban',
            fields=[
                (
                    'id', models.AutoField(
                        verbose_name='ID', serialize=False, auto_created=True, primary_key=True
                    )
                ),
                ('check_type', models.PositiveIntegerField(default=0, db_index=True)),
                ('banned_value', models.CharField(max_length=255, db_index=True)),
                ('user_message', models.TextField(null=True, blank=True)),
                ('staff_message', models.TextField(null=True, blank=True)),
                ('expires_on', models.DateTimeField(null=True, blank=True, db_index=True)),
                ('is_checked', models.BooleanField(default=True, db_index=True)),
            ],
            bases=(models.Model, ),
        ),
        migrations.CreateModel(
            name='BanCache',
            fields=[
                ('user_message', models.TextField(null=True, blank=True)),
                ('staff_message', models.TextField(null=True, blank=True)),
                ('bans_version', models.PositiveIntegerField(default=0)),
                ('expires_on', models.DateTimeField(null=True, blank=True)),
                (
                    'ban', models.ForeignKey(
                        on_delete=django.db.models.deletion.SET_NULL,
                        blank=True,
                        to='misago_users.Ban',
                        null=True
                    )
                ),
                (
                    'user', models.OneToOneField(
                        related_name='ban_cache',
                        on_delete=django.db.models.deletion.CASCADE,
                        primary_key=True,
                        serialize=False,
                        to=settings.AUTH_USER_MODEL
                    )
                ),
            ],
            options={},
            bases=(models.Model, ),
        ),
    ]
