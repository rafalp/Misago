# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('misago_threads', '0001_initial'),
        ('misago_forums', '0003_forums_roles'),
    ]

    operations = [
        migrations.AddField(
            model_name='forum',
            name='last_thread',
            field=models.ForeignKey(related_name=b'+', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='misago_threads.Thread', null=True),
            preserve_default=True,
        ),
    ]
