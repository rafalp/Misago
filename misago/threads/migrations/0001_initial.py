# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('misago_forums', '0001_initial'),
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
    ]
