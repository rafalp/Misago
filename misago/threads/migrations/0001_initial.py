# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('misago_forums', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Prefix',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField(max_length=255)),
                ('css_class', models.CharField(max_length=255, null=True, blank=True)),
                ('forums', models.ManyToManyField(related_name=b'prefixes', to='misago_forums.Forum')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('poster_name', models.CharField(max_length=255)),
                ('poster_ip', models.GenericIPAddressField()),
                ('original', models.TextField()),
                ('parsed', models.TextField()),
                ('checksum', models.CharField(max_length=64)),
                ('has_attachments', models.BooleanField(default=False)),
                ('pickled_attachments', models.TextField(null=True, blank=True)),
                ('posted_on', models.DateTimeField()),
                ('updated_on', models.DateTimeField()),
                ('edits', models.PositiveIntegerField(default=0)),
                ('last_editor_name', models.CharField(max_length=255, null=True, blank=True)),
                ('last_editor_slug', models.SlugField(max_length=255, null=True, blank=True)),
                ('is_reported', models.BooleanField(default=False, db_index=True)),
                ('is_moderated', models.BooleanField(default=False)),
                ('is_hidden', models.BooleanField(default=False)),
                ('is_protected', models.BooleanField(default=False)),
                ('forum', models.ForeignKey(to='misago_forums.Forum')),
                ('last_editor', models.ForeignKey(related_name=b'+', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('mentions', models.ManyToManyField(related_name=b'mention_set', to=settings.AUTH_USER_MODEL)),
                ('poster', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Thread',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('weight', models.PositiveIntegerField(default=0)),
                ('title', models.CharField(max_length=255)),
                ('slug', models.SlugField(max_length=255)),
                ('replies', models.PositiveIntegerField(default=0)),
                ('has_reported_posts', models.BooleanField(default=False)),
                ('has_moderated_posts', models.BooleanField(default=False)),
                ('has_hidden_posts', models.BooleanField(default=False)),
                ('started_on', models.DateTimeField(db_index=True)),
                ('starter_name', models.CharField(max_length=255)),
                ('starter_slug', models.SlugField(max_length=255)),
                ('last_post_on', models.DateTimeField(db_index=True)),
                ('last_poster_name', models.CharField(max_length=255, null=True, blank=True)),
                ('last_poster_slug', models.SlugField(max_length=255, null=True, blank=True)),
                ('is_poll', models.BooleanField(default=False)),
                ('is_moderated', models.BooleanField(default=False)),
                ('is_hidden', models.BooleanField(default=False)),
                ('is_closed', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='post',
            name='thread',
            field=models.ForeignKey(to='misago_threads.Thread'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='thread',
            name='first_post',
            field=models.ForeignKey(related_name=b'+', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='misago_threads.Post', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='thread',
            name='forum',
            field=models.ForeignKey(to='misago_forums.Forum'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='thread',
            name='last_post',
            field=models.ForeignKey(related_name=b'+', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='misago_threads.Post', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='thread',
            name='last_poster',
            field=models.ForeignKey(related_name=b'+', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='thread',
            name='prefix',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='misago_threads.Prefix', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='thread',
            name='starter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
]
