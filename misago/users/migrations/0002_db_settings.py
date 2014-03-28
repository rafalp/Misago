# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models
from misago.conf.migrationutils import migrate_settings_group, with_conf_models
from misago.core.migrationutils import ugettext_lazy as _


class Migration(DataMigration):

    def forwards(self, orm):
        "Write your forwards methods here."
        migrate_settings_group(
            orm,
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
                        'value': 3,
                        'field_extra': {
                            'min_value': 2,
                            'max_value': 255,
                        },
                    },
                    {
                        'setting': 'password_complexity',
                        'name': _("Complexity"),
                        'python_type': 'list',
                        'value': [],
                        'form_field': 'checkbox',
                        'field_extra': {
                            'choices': (
                                ('case', _("Require mixed Case")),
                                ('alphanumerics', _("Require alphanumeric characters")),
                                ('special', _("Require special characters"))
                            ),
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
            },
        )


    def backwards(self, orm):
        "Write your backwards methods here."

    models = with_conf_models('0001_initial')

    complete_apps = ['core']
    symmetrical = True

    depends_on = (
        ("conf", "0001_initial"),
    )
