# -*- coding: utf-8 -*-
from django.db import migrations

from .. import ACL_CACHE
from ...cache.operations import StartCacheVersioning


class Migration(migrations.Migration):

    dependencies = [
        ("misago_acl", "0003_default_roles"),
        ("misago_cache", "0001_initial"),
    ]

    operations = [StartCacheVersioning(ACL_CACHE)]
