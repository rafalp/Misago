# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.translation import ugettext as _
from misago.conf.migrationutils import migrate_settings_group


def create_users_settings_group(apps, schema_editor):
    migrate_settings_group(
        apps,
        {
            'key': 'users',
            'name': _("Users"),
            'settings': (
                {
                    'setting': 'account_activation',
                    'name': _("New accounts activation"),
                    'legend': _("New accounts"),
                    'value': 'none',
                    'form_field': 'select',
                    'field_extra': {
                        'choices': (
                            ('none', _("No activation required")),
                            ('user', _("Activation Token sent to User")),
                            ('admin', _("Activation by Administrator")),
                            ('block', _("Don't allow new registrations"))
                        )
                    },
                },
                {
                    'setting': 'default_timezone',
                    'name': _("Default timezone"),
                    'description': _("Default timezone for newly "
                                     "registered accouts as well as "
                                     "unsigned users."),
                    'value': 'utc',
                    'form_field': 'select',
                    'field_extra': {
                        'choices': '#TZ#',
                    },
                },
                {
                    'setting': 'username_length_min',
                    'name': _("Minimal allowed username length"),
                    'legend': _("User names"),
                    'python_type': 'int',
                    'value': 3,
                    'field_extra': {
                        'min_value': 2,
                        'max_value': 255,
                    },
                },
                {
                    'setting': 'username_length_max',
                    'name': _("Maximal allowed username length"),
                    'python_type': 'int',
                    'value': 14,
                    'field_extra': {
                        'min_value': 2,
                        'max_value': 255,
                    },
                },
                {
                    'setting': 'password_length_min',
                    'name': _("Minimum user password length"),
                    'legend': _("Passwords"),
                    'python_type': 'int',
                    'value': 5,
                    'field_extra': {
                        'min_value': 2,
                        'max_value': 255,
                    },
                },
                {
                    'setting': 'avatars_types',
                    'name': _("Available avatar types"),
                    'legend': _("Avatars"),
                    'python_type': 'list',
                    'value': ['gravatar', 'upload'],
                    'form_field': 'checkbox',
                    'field_extra': {
                        'choices': (
                            ('gravatar', _("Gravatar")),
                            ('upload', _("Uploaded avatar")),
                            ('gallery', _("Avatars gallery"))
                        ),
                        'min': 1,
                    },
                },
                {
                    'setting': 'default_avatar',
                    'name': _("Default avatar"),
                    'value': 'gravatar',
                    'form_field': 'select',
                    'field_extra': {
                        'choices': (
                            ('gravatar', _("Gravatar")),
                            ('gallery', _("Random avatar from gallery")),
                        ),
                    },
                },
                {
                    'setting': 'avatar_upload_limit',
                    'name': _("Maximum size of uploaded avatar"),
                    'description': _("Enter maximum allowed file size "
                                     "(in KB) for avatar uploads"),
                    'python_type': 'int',
                    'value': 128,
                    'field_extra': {
                        'min_value': 0,
                    },
                },
                {
                    'setting': 'subscribe_start',
                    'name': _("Subscribe to started threads"),
                    'legend': _("Default subscriptions settings"),
                    'value': 'watch_email',
                    'form_field': 'select',
                    'field_extra': {
                        'choices': (
                            ('no', _("Don't watch")),
                            ('', _("Put on watched threads list")),
                            ('watch_email', _("Put on watched threads "
                                              "list and e-mail user when "
                                              "somebody replies")),
                        ),
                    },
                },
                {
                    'setting': 'subscribe_reply',
                    'name': _("Subscribe to replied threads"),
                    'value': 'watch_email',
                    'form_field': 'select',
                    'field_extra': {
                        'choices': (
                            ('no', _("Don't watch")),
                            ('', _("Put on watched threads list")),
                            ('watch_email', _("Put on watched threads "
                                              "list and e-mail user when "
                                              "somebody replies")),
                        ),
                    },
                },
            )
        })


class Migration(migrations.Migration):

    dependencies = [
        ('misago_users', '0001_initial'),
        ('misago_conf', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_users_settings_group),
    ]
