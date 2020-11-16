from django.db import migrations

from .. import SOCIALAUTH_CACHE
from ...cache.operations import StartCacheVersioning


class Migration(migrations.Migration):

    dependencies = [
        ("misago_socialauth", "0001_initial"),
        ("misago_cache", "0001_initial"),
    ]

    operations = [StartCacheVersioning(SOCIALAUTH_CACHE)]
