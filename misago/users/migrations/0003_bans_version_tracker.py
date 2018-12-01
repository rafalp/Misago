from django.db import migrations


def register_bans_version_tracker(apps, schema_editor):
    from misago.core.migrationutils import cachebuster_register_cache
    cachebuster_register_cache(apps, "misago_bans")


class Migration(migrations.Migration):
    """Migration superseded by 0016"""

    dependencies = [
        ('misago_users', '0002_users_settings'),
        ('misago_core', '0001_initial'),
    ]

    operations = [
        # FIXME: remove this operation
        migrations.RunPython(register_bans_version_tracker),
    ]
