# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations

from misago.acl.constants import ACL_CACHEBUSTER
from misago.core.migrationutils import cachebuster_register_cache


def register_acl_version_tracker(apps, schema_editor):
    cachebuster_register_cache(apps, ACL_CACHEBUSTER)


class Migration(migrations.Migration):

    dependencies = [
        ('misago_acl', '0001_initial'),
        ('misago_core', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(register_acl_version_tracker),
    ]
