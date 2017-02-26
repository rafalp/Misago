# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations

from misago.conf.migrationutils import migrate_settings_group


_ = lambda x: x


def create_users_settings_group(apps, schema_editor):
    migrate_settings_group(
        apps, {
            'key': 'users',
            'name': _("Users"),
            'description': _(
                "Those settings control user accounts default behaviour and features availability."
            ),
            'settings': [
                {
                    'setting': 'account_activation',
                    'name': _("New accounts activation"),
                    'legend': _("New accounts"),
                    'value': 'none',
                    'form_field': 'select',
                    'field_extra': {
                        'choices': [
                            ('none', _("No activation required")),
                            ('user', _("Activation token sent to User")),
                            ('admin', _("Activation by administrator")),
                            ('closed', _("Don't allow new registrations")),
                        ],
                    },
                    'is_public': True,
                },
                {
                    'setting': 'username_length_min',
                    'name': _("Minimum length"),
                    'description': _("Minimum allowed username length."),
                    'legend': _("User names"),
                    'python_type': 'int',
                    'value': 3,
                    'field_extra': {
                        'min_value': 2,
                        'max_value': 20,
                    },
                    'is_public': True,
                },
                {
                    'setting': 'username_length_max',
                    'name': _("Maximum length"),
                    'description': _("Maximum allowed username length."),
                    'python_type': 'int',
                    'value': 14,
                    'field_extra': {
                        'min_value': 2,
                        'max_value': 20,
                    },
                    'is_public': True,
                },
                {
                    'setting': 'password_length_min',
                    'name': _("Minimum length"),
                    'description': _("Minimum allowed user password length."),
                    'legend': _("Passwords"),
                    'python_type': 'int',
                    'value': 5,
                    'field_extra': {
                        'min_value': 2,
                        'max_value': 255,
                    },
                    'is_public': True,
                },
                {
                    'setting': 'allow_custom_avatars',
                    'name': _("Allow custom avatars"),
                    'legend': _("Avatars"),
                    'description': _(
                        "Turning this option off will forbid "
                        "forum users from using avatars from "
                        "outside forums. Good for forums "
                        "adressed at young users."
                    ),
                    'python_type': 'bool',
                    'value': True,
                    'form_field': 'yesno',
                },
                {
                    'setting': 'default_avatar',
                    'name': _("Default avatar"),
                    'value': 'gravatar',
                    'form_field': 'select',
                    'field_extra': {
                        'choices': [
                            ('dynamic', _("Individual")),
                            ('gravatar', _("Gravatar")),
                            ('gallery', _("Random avatar from gallery")),
                        ],
                    },
                },
                {
                    'setting': 'default_gravatar_fallback',
                    'name': _("Fallback for default gravatar"),
                    'description': _(
                        "Select which avatar to use when user has no "
                        "gravatar associated with his e-mail address."
                    ),
                    'value': 'dynamic',
                    'form_field': 'select',
                    'field_extra': {
                        'choices': [
                            ('dynamic', _("Individual")),
                            ('gallery', _("Random avatar from gallery")),
                        ],
                    },
                },
                {
                    'setting': 'avatar_upload_limit',
                    'name': _("Maximum size of uploaded avatar"),
                    'description': _("Enter maximum allowed file size (in KB) for avatar uploads."),
                    'python_type': 'int',
                    'value': 1536,
                    'field_extra': {
                        'min_value': 0,
                    },
                    'is_public': True,
                },
                {
                    'setting': 'signature_length_max',
                    'name': _("Maximum length"),
                    'legend': _("Signatures"),
                    'description': _("Maximum allowed signature length."),
                    'python_type': 'int',
                    'value': 256,
                    'field_extra': {
                        'min_value': 10,
                        'max_value': 5000,
                    },
                    'is_public': True,
                },
                {
                    'setting': 'subscribe_start',
                    'name': _("Started threads"),
                    'legend': _("Default subscriptions settings"),
                    'value': 'watch_email',
                    'form_field': 'select',
                    'field_extra': {
                        'choices': [
                            ('no', _("Don't watch")),
                            ('watch', _("Put on watched threads list")),
                            (
                                'watch_email', _(
                                    "Put on watched threads "
                                    "list and e-mail user when "
                                    "somebody replies"
                                )
                            ),
                        ],
                    },
                },
                {
                    'setting': 'subscribe_reply',
                    'name': _("Replied threads"),
                    'value': 'watch_email',
                    'form_field': 'select',
                    'field_extra': {
                        'choices': [
                            ('no', _("Don't watch")),
                            ('watch', _("Put on watched threads list")),
                            (
                                'watch_email', _(
                                    "Put on watched threads "
                                    "list and e-mail user when "
                                    "somebody replies"
                                )
                            ),
                        ],
                    },
                },
            ],
        }
    )

    migrate_settings_group(
        apps, {
            'key': 'captcha',
            'name': _("CAPTCHA"),
            'description': _("Those settings allow you to combat automatic registrations on your forum."),
            'settings': [
                {
                    'setting': 'captcha_type',
                    'name': _("Select CAPTCHA type"),
                    'legend': _("CAPTCHA type"),
                    'value': 'no',
                    'form_field': 'select',
                    'field_extra': {
                        'choices': [
                            ('no', _("No CAPTCHA")),
                            ('re', _("reCaptcha")),
                            ('qa', _("Question and answer")),
                        ],
                    },
                    'is_public': True,
                },
                {
                    'setting': 'recaptcha_site_key',
                    'name': _("Site key"),
                    'legend': _("reCAPTCHA"),
                    'value': '',
                    'field_extra': {
                        'required': False,
                        'max_length': 100,
                    },
                    'is_public': True,
                },
                {
                    'setting': 'recaptcha_secret_key',
                    'name': _("Secret key"),
                    'value': '',
                    'field_extra': {
                        'required': False,
                        'max_length': 100,
                    },
                },
                {
                    'setting': 'qa_question',
                    'name': _("Test question"),
                    'legend': _("Question and answer"),
                    'value': '',
                    'field_extra': {
                        'required': False,
                        'max_length': 250,
                    },
                },
                {
                    'setting': 'qa_help_text',
                    'name': _("Question help text"),
                    'value': '',
                    'field_extra': {
                        'required': False,
                        'max_length': 250,
                    },
                },
                {
                    'setting': 'qa_answers',
                    'name': _("Valid answers"),
                    'description': _("Enter each answer in new line. Answers are case-insensitive."),
                    'value': '',
                    'form_field': 'textarea',
                    'field_extra': {
                        'rows': 4,
                        'required': False,
                        'max_length': 250,
                    },
                },
            ],
        }
    )


class Migration(migrations.Migration):

    dependencies = [
        ('misago_users', '0001_initial'),
        ('misago_conf', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_users_settings_group),
    ]
