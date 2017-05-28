# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('misago_threads', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CategoryRead',
            fields=[
                (
                    'id', models.AutoField(
                        verbose_name='ID', serialize=False, auto_created=True, primary_key=True
                    )
                ),
                ('last_read_on', models.DateTimeField()),
                (
                    'category', models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to='misago_categories.Category',
                    )
                ),
                (
                    'user', models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    )
                ),
            ],
            options={},
            bases=(models.Model, ),
        ),
        migrations.CreateModel(
            name='ThreadRead',
            fields=[
                (
                    'id', models.AutoField(
                        verbose_name='ID', serialize=False, auto_created=True, primary_key=True
                    )
                ),
                ('last_read_on', models.DateTimeField()),
                (
                    'category', models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to='misago_categories.Category',
                    )
                ),
                (
                    'thread', models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to='misago_threads.Thread',
                    )
                ),
                (
                    'user', models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    )
                ),
            ],
            options={},
            bases=(models.Model, ),
        ),
    ]
