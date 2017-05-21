# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations

from misago.conf.migrationutils import migrate_settings_group


_ = lambda x: x


def create_legal_settings_group(apps, schema_editor):
    migrate_settings_group(
        apps, {
            'key': 'legal',
            'name': _("Legal information"),
            'description': _("Those settings allow you to set forum terms of service and privacy policy."),
            'settings': [
                {
                    'setting': 'terms_of_service_title',
                    'name': _("Terms title"),
                    'legend': _("Terms of Service"),
                    'description': _("Leave this field empty to use default title."),
                    'value': "",
                    'field_extra': {
                        'max_length': 255,
                        'required': False,
                    },
                    'is_public': True,
                },
                {
                    'setting': 'terms_of_service_link',
                    'name': _("Terms link"),
                    'description': _("If terms of service are located on other page, enter there its link."),
                    'value': "",
                    'field_extra': {
                        'max_length': 255,
                        'required': False,
                    },
                    'is_public': True,
                },
                {
                    'setting': 'terms_of_service',
                    'name': _("Terms contents"),
                    'description': _(
                        "Your forums can have custom terms of "
                        "service page. To create it, write or "
                        "paste here its contents. Full Misago "
                        "markup is available for formatting."
                    ),
                    'value': "",
                    'form_field': 'textarea',
                    'field_extra': {
                        'max_length': 128000,
                        'required': False,
                        'rows': 8,
                    },
                    'is_public': True,
                    'is_lazy': True,
                },
                {
                    'setting': 'privacy_policy_title',
                    'name': _("Policy title"),
                    'legend': _("Privacy policy"),
                    'description': _("Leave this field empty to use default title."),
                    'value': "",
                    'field_extra': {
                        'max_length': 255,
                        'required': False,
                    },
                    'is_public': True,
                },
                {
                    'setting': 'privacy_policy_link',
                    'name': _("Policy link"),
                    'description': _("If privacy policy is located on other page, enter there its link."),
                    'value': "",
                    'field_extra': {
                        'max_length': 255,
                        'required': False,
                    },
                    'is_public': True,
                },
                {
                    'setting': 'privacy_policy',
                    'name': _("Policy contents"),
                    'description': _(
                        "Your forums can have custom privacy "
                        "policy page. To create it, write or "
                        "paste here its contents. Full Misago "
                        "markup is available for formatting."
                    ),
                    'value': "",
                    'form_field': 'textarea',
                    'field_extra': {
                        'max_length': 128000,
                        'required': False,
                        'rows': 8,
                    },
                    'is_public': True,
                    'is_lazy': True,
                },
                {
                    'setting': 'forum_footnote',
                    'name': _("Footnote"),
                    'description': _("Short message displayed in forum footer."),
                    'legend': _("Forum footer"),
                    'field_extra': {
                        'max_length': 300,
                    },
                    'is_public': True,
                },
            ],
        }
    )


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('misago_conf', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_legal_settings_group),
    ]
