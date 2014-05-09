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
                        'name': _("Forum index title"),
                        'description': _("You may set custon title on "
                                         "forum index by typing it here."),
                        'legend': _("Forum index"),
                        'field_extra': {
                            'max_length': 255
                        },
                    },
                    {
                        'setting': 'forum_index_meta_description',
                        'name': _("Forum index Meta Description"),
                        'description': _("Short description of your forum "
                                         "for internet crawlers."),
                        'field_extra': {
                            'max_length': 255
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
