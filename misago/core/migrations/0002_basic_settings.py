# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations

from misago.conf.migrationutils import migrate_settings_group


_ = lambda x: x


def create_basic_settings_group(apps, schema_editor):
    migrate_settings_group(
        apps, {
            'key': 'basic',
            'name': _("Basic forum settings"),
            'description': _(
                "Those settings control most basic properties "
                "of your forum like its name or description."
            ),
            'settings': [
                {
                    'setting': 'forum_name',
                    'name': _("Forum name"),
                    'legend': _("General"),
                    'value': "Misago",
                    'field_extra': {
                        'min_length': 2,
                        'max_length': 255
                    },
                    'is_public': True,
                },
                {
                    'setting': 'forum_index_title',
                    'name': _("Index title"),
                    'description': _("You may set custon title on forum index by typing it here."),
                    'legend': _("Forum index"),
                    'field_extra': {
                        'max_length': 255
                    },
                    'is_public': True,
                },
                {
                    'setting': 'forum_index_meta_description',
                    'name': _("Meta Description"),
                    'description': _("Short description of your forum for internet crawlers."),
                    'field_extra': {
                        'max_length': 255
                    },
                },
                {
                    'setting': 'forum_branding_display',
                    'name': _("Display branding"),
                    'description': _("Switch branding in forum's navbar."),
                    'legend': _("Branding"),
                    'value': True,
                    'python_type': 'bool',
                    'form_field': 'yesno',
                    'is_public': True,
                },
                {
                    'setting': 'forum_branding_text',
                    'name': _("Branding text"),
                    'description': _("Optional text displayed besides brand image in navbar."),
                    'value': "Misago",
                    'field_extra': {
                        'max_length': 255
                    },
                    'is_public': True,
                },
                {
                    'setting': 'email_footer',
                    'name': _("E-mails footer"),
                    'description': _("Optional short message included at the end of e-mails sent by forum."),
                    'legend': _("Forum e-mails"),
                    'field_extra': {
                        'max_length': 255
                    },
                },
            ],
        }
    )


class Migration(migrations.Migration):

    dependencies = [
        ('misago_core', '0001_initial'),
        ('misago_conf', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_basic_settings_group),
    ]
