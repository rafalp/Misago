# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Setting',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('setting', models.CharField(unique=True, max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(null=True, blank=True)),
                ('legend', models.CharField(max_length=255, null=True, blank=True)),
                ('order', models.IntegerField(default=0, db_index=True)),
                ('dry_value', models.TextField(null=True, blank=True)),
                ('default_value', models.TextField(null=True, blank=True)),
                ('python_type', models.CharField(default=b'string', max_length=255)),
                ('is_lazy', models.BooleanField(default=False)),
                ('form_field', models.CharField(default=b'text', max_length=255)),
                ('pickled_field_extra', models.TextField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SettingsGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('key', models.CharField(unique=True, max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='setting',
            name='group',
            field=models.ForeignKey(to='misago_conf.SettingsGroup', to_field='id'),
            preserve_default=True,
        ),
    ]
