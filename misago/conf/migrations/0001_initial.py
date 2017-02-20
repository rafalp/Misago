# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.postgres.fields import JSONField
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Setting',
            fields=[
                (
                    'id', models.AutoField(
                        verbose_name='ID', serialize=False, auto_created=True, primary_key=True
                    )
                ),
                ('setting', models.CharField(unique=True, max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(null=True, blank=True)),
                ('legend', models.CharField(max_length=255, null=True, blank=True)),
                ('order', models.IntegerField(default=0, db_index=True)),
                ('dry_value', models.TextField(null=True, blank=True)),
                ('default_value', models.TextField(null=True, blank=True)),
                ('python_type', models.CharField(default='string', max_length=255)),
                ('is_public', models.BooleanField(default=False)),
                ('is_lazy', models.BooleanField(default=False)),
                ('form_field', models.CharField(default='text', max_length=255)),
                ('field_extra', JSONField()),
            ],
            options={},
            bases=(models.Model, ),
        ),
        migrations.CreateModel(
            name='SettingsGroup',
            fields=[
                (
                    'id', models.AutoField(
                        verbose_name='ID', serialize=False, auto_created=True, primary_key=True
                    )
                ),
                ('key', models.CharField(unique=True, max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(null=True, blank=True)),
            ],
            options={},
            bases=(models.Model, ),
        ),
        migrations.AddField(
            model_name='setting',
            name='group',
            field=models.ForeignKey(to='misago_conf.SettingsGroup', to_field='id'),
            preserve_default=True,
        ),
    ]
