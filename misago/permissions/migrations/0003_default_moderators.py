# Generated by Django 4.2.8 on 2024-01-02 12:10

from django.db import migrations

from ...users.enums import DefaultGroupId


DEFAULT_MODERATOR_GROUPS = (DefaultGroupId.ADMINS, DefaultGroupId.MODERATORS)


def create_default_moderators(apps, schema_editor):
    Moderator = apps.get_model("misago_permissions", "Moderator")

    for group_id in DEFAULT_MODERATOR_GROUPS:
        Moderator.objects.create(
            group_id=group_id,
            is_global=True,
        )


class Migration(migrations.Migration):
    dependencies = [
        ("misago_permissions", "0002_default_category_permissions"),
    ]

    operations = [
        migrations.RunPython(
            create_default_moderators,
            migrations.RunPython.noop,
        ),
    ]
