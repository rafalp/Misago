# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
from django.utils.translation import ugettext as _

from misago.conf.migrationutils import migrate_settings_group


def create_threads_settings_group(apps, schema_editor):
    migrate_settings_group(
        apps,
        {
            'key': 'threads',
            'name': _("Threads"),
            'description': _("Those settings control threads and posts."),
            'settings': (
                {
                    'setting': 'thread_title_length_min',
                    'name': _("Minimum length"),
                    'description': _("Minimum allowed thread title length."),
                    'legend': _("Thread titles"),
                    'python_type': 'int',
                    'value': 5,
                    'field_extra': {
                        'min_value': 2,
                        'max_value': 255,
                    },
                    'is_public': True,
                },
                {
                    'setting': 'thread_title_length_max',
                    'name': _("Maximum length"),
                    'description': _("Maximum allowed thread length."),
                    'python_type': 'int',
                    'value': 90,
                    'field_extra': {
                        'min_value': 2,
                        'max_value': 255,
                    },
                    'is_public': True,
                },
                {
                    'setting': 'post_length_min',
                    'name': _("Minimum length"),
                    'description': _("Minimum allowed user post length."),
                    'legend': _("Posts"),
                    'python_type': 'int',
                    'value': 5,
                    'field_extra': {
                        'min_value': 1,
                    },
                },
                {
                    'setting': 'post_length_max',
                    'name': _("Maximum length"),
                    'description': _("Maximum allowed user post length. Enter zero to disable"),
                    'python_type': 'int',
                    'value': 60000,
                    'field_extra': {
                        'min_value': 0,
                    },
                },
            )
        })


class Migration(migrations.Migration):

    dependencies = [
        ('misago_threads', '0001_initial'),
        ('misago_conf', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_threads_settings_group),
    ]
