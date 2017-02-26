# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations

from misago.conf.migrationutils import delete_settings_cache, migrate_settings_group


_ = lambda x: x


def update_threads_settings(apps, schema_editor):
    migrate_settings_group(
        apps, {
            'key': 'threads',
            'name': _("Threads"),
            'description': _("Those settings control threads and posts."),
            'settings': [
                {
                    'setting': 'thread_title_length_min',
                    'name': _("Minimum length"),
                    'description': _("Minimum allowed thread title length."),
                    'legend': _("Thread titles"),
                    'python_type': 'int',
                    'default_value': 5,
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
                    'default_value': 90,
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
                    'default_value': 5,
                    'field_extra': {
                        'min_value': 1,
                    },
                    'is_public': True,
                },
                {
                    'setting': 'post_length_max',
                    'name': _("Maximum length"),
                    'description': _(
                        "Maximum allowed user post length. Enter zero to disable. "
                        "Longer posts are more costful to parse and index."
                    ),
                    'python_type': 'int',
                    'default_value': 60000,
                    'field_extra': {
                        'min_value': 0,
                    },
                    'is_public': True,
                },
            ],
        }
    )

    delete_settings_cache()


class Migration(migrations.Migration):

    dependencies = [
        ('misago_threads', '0003_attachment_types'),
    ]

    operations = [
        migrations.RunPython(update_threads_settings),
    ]
