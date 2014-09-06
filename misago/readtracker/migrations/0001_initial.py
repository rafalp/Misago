# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('misago_threads', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ForumRead',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('last_updated_on', models.DateTimeField()),
                ('last_cleared_on', models.DateTimeField()),
                ('forum', models.ForeignKey(to='misago_forums.Forum')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ThreadRead',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('read_replies', models.PositiveIntegerField(default=0)),
                ('last_read_on', models.DateTimeField()),
                ('forum', models.ForeignKey(to='misago_forums.Forum')),
                ('thread', models.ForeignKey(to='misago_threads.Thread')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
