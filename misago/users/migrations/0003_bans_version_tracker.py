# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations

from misago.core.migrationutils import cachebuster_register_cache
from misago.users.constants import BANS_CACHEBUSTER


def register_bans_version_tracker(apps, schema_editor):
    cachebuster_register_cache(apps, BANS_CACHEBUSTER)


class Migration(migrations.Migration):

    dependencies = [
        ('misago_users', '0002_users_settings'),
        ('misago_core', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(register_bans_version_tracker),
    ]
