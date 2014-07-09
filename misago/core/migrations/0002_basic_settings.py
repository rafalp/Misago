# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.translation import ugettext as _

from misago.conf.migrationutils import migrate_settings_group


def create_basic_settings_group(apps, schema_editor):
    migrate_settings_group(
        apps,
        {
            'key': 'basic',
            'name': _("Basic forum settings"),
            'description': _("Those settings control most basic properties "
                             "of your forum like its name or description."),
            'settings': (
                {
                    'setting': 'forum_name',
                    'name': _("Forum name"),
                    'legend': _("General"),
                    'value': "Misago",
                    'field_extra': {
                        'min_length': 2,
                        'max_length': 255
                    },
                },
                {
                    'setting': 'forum_index_title',
                    'name': _("Index title"),
                    'description': _("You may set custon title on "
                                     "forum index by typing it here."),
                    'legend': _("Forum index"),
                    'field_extra': {
                        'max_length': 255
                    },
                },
                {
                    'setting': 'forum_index_meta_description',
                    'name': _("Meta Description"),
                    'description': _("Short description of your forum "
                                     "for internet crawlers."),
                    'field_extra': {
                        'max_length': 255
                    },
                },
                {
                    'setting': 'email_footer',
                    'name': _("E-mails footer"),
                    'description': _("Optional short message included "
                                     "at the end of e-mails sent by "
                                     "forum"),
                    'legend': _("Forum e-mails"),
                    'field_extra': {
                        'max_length': 255
                    },
                },
            )
        })

    migrate_settings_group(
        apps,
        {
            'key': 'captcha',
            'name': _("CAPTCHA"),
            'description': _("Those settings allow you to combat automatic "
                             "registrations and spam messages on your forum."),
            'settings': (
                {
                    'setting': 'captcha_on_registration',
                    'name': _("CAPTCHA on registration"),
                    'legend': _("CAPTCHA types"),
                    'value': 'no',
                    'form_field': 'select',
                    'field_extra': {
                        'choices': (
                            ('no', _("No protection")),
                            ('recaptcha', _("reCaptcha")),
                            ('qa', _("Question and answer")),
                        ),
                    },
                },
                {
                    'setting': 'recaptcha_public_api_key',
                    'name': _("Public API key"),
                    'legend': _("reCAPTCHA"),
                    'value': '',
                    'field_extra': {
                        'required': False,
                        'max_length': 100,
                    },
                },
                {
                    'setting': 'recaptcha_private_api_key',
                    'name': _("Private API key"),
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
                    'description': _("Enter each answer in new line. "
                                     "Answers are case-insensitive."),
                    'value': '',
                    'form_field': 'textarea',
                    'field_extra': {
                        'rows': 4,
                        'required': False,
                        'max_length': 250,
                    },
                },
            )
        })


class Migration(migrations.Migration):

    dependencies = [
        ('misago_core', '0001_initial'),
        ('misago_conf', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_basic_settings_group),
    ]
