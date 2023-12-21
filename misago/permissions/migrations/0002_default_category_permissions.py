# Generated by Django 4.2.7 on 2023-12-21 22:37

from django.db import migrations

from ...users.enums import DefaultGroupId
from ..enums import CategoryPermission


FULL_CATEGORY_PERMISSIONS = (
    CategoryPermission.SEE,
    CategoryPermission.READ,
    CategoryPermission.START,
    CategoryPermission.REPLY,
    CategoryPermission.ATTACHMENTS,
)

GUEST_CATEGORY_PERMISSIONS = (
    CategoryPermission.SEE,
    CategoryPermission.READ,
    CategoryPermission.ATTACHMENTS,
)

GROUPS_PERMISSIONS = {
    DefaultGroupId.ADMINS: FULL_CATEGORY_PERMISSIONS,
    DefaultGroupId.MODERATORS: FULL_CATEGORY_PERMISSIONS,
    DefaultGroupId.MEMBERS: FULL_CATEGORY_PERMISSIONS,
    DefaultGroupId.GUESTS: GUEST_CATEGORY_PERMISSIONS,
}


def create_default_category_permissions(apps, schema_editor):
    Permission = apps.get_model("misago_permissions", "CategoryPermission")
    Category = apps.get_model("misago_categories", "Category")

    try:
        category = Category.objects.get(slug="first-category")
    except Category.DoesNotExist:
        return

    bulk_create_data: list[Permission] = []
    for group_id, group_permissions in GROUPS_PERMISSIONS.items():
        for permission in group_permissions:
            bulk_create_data.append(
                Permission(
                    category_id=category.id,
                    group_id=group_id,
                    permission=permission.name,
                )
            )

    Permission.objects.bulk_create(bulk_create_data)


class Migration(migrations.Migration):
    dependencies = [
        ("misago_permissions", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(
            create_default_category_permissions,
            migrations.RunPython.noop,
        ),
    ]
