from django.db import migrations


def register_acl_version_tracker(apps, schema_editor):
    from misago.core.migrationutils import cachebuster_register_cache
    cachebuster_register_cache(apps, "misago_acl")


class Migration(migrations.Migration):
    """Superseded by 0004"""

    dependencies = [
        ('misago_acl', '0001_initial'),
        ('misago_core', '0001_initial'),
    ]

    operations = [
        # FIXME: remove this operation
        migrations.RunPython(register_acl_version_tracker),
    ]
