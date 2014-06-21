# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0002_auto_20140620_2207'),
        ('misago_acl', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(max_length=30)),
                ('username_slug', models.CharField(unique=True, max_length=30)),
                ('email', models.EmailField(max_length=255, db_index=True)),
                ('email_hash', models.CharField(unique=True, max_length=32)),
                ('joined_on', models.DateTimeField(default=django.utils.timezone.now, verbose_name='joined on')),
                ('title', models.CharField(max_length=255, null=True, blank=True)),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into admin sites.', db_index=True, verbose_name='staff status')),
                ('acl_key', models.CharField(max_length=12, null=True, blank=True)),
                ('groups', models.ManyToManyField(to='auth.Group', verbose_name='groups', blank=True)),
                ('roles', models.ManyToManyField(to='misago_acl.Role')),
                ('user_permissions', models.ManyToManyField(to='auth.Permission', verbose_name='user permissions', blank=True)),
            ],
            options={
                'abstract': False,
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
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to_field='id', blank=True, to='misago_users.Rank', null=True),
            preserve_default=True,
        ),
    ]
