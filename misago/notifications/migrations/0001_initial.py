# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_new', models.BooleanField(default=True)),
                ('date', models.DateTimeField(default=django.utils.timezone.now, db_index=True)),
                ('trigger', models.CharField(max_length=8)),
                ('message', models.TextField()),
                ('url', models.TextField()),
                ('sender_username', models.CharField(max_length=255, null=True, blank=True)),
                ('sender_slug', models.CharField(max_length=255, null=True, blank=True)),
                ('sender', models.ForeignKey(related_name=b'notifications_by', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('user', models.ForeignKey(related_name=b'notifications', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
