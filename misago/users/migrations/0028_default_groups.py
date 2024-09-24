# Generated by Django 4.2.7 on 2023-12-21 21:10

from django.db import migrations

from ...permissions.permissionsid import get_permissions_id
from ..enums import CUSTOM_GROUP_ID_START, DefaultGroupId


def pgettext(context: str, message: str):
    return message


def create_default_groups(apps, schema_editor):
    Group = apps.get_model("misago_users", "Group")
    groups = Group.objects.bulk_create(
        [
            Group(
                id=DefaultGroupId.ADMINS,
                name=pgettext("default user group", "Administrators"),
                slug="administrators",
                user_title=pgettext("default user group", "Admin"),
                color="#6554C0",
                icon="fas fa-shield",
                css_suffix="admin",
                is_page=True,
                ordering=0,
                # Permissions
                can_use_private_threads=True,
                can_start_private_threads=True,
                private_thread_users_limit=20,
                can_edit_own_threads=True,
                own_threads_edit_time_limit=0,
                can_edit_own_posts=True,
                own_posts_edit_time_limit=0,
                can_change_username=True,
                can_see_user_profiles=True,
            ),
            Group(
                id=DefaultGroupId.MODERATORS,
                name=pgettext("default user group", "Moderators"),
                slug="moderators",
                user_title=pgettext("default user group", "Moderator"),
                color="#00875A",
                icon="fas fa-shield",
                css_suffix="moderator",
                is_page=True,
                ordering=1,
                # Permissions
                can_use_private_threads=True,
                can_start_private_threads=True,
                private_thread_users_limit=20,
                can_edit_own_threads=True,
                own_threads_edit_time_limit=0,
                can_edit_own_posts=True,
                own_posts_edit_time_limit=0,
                can_change_username=True,
                can_see_user_profiles=True,
            ),
            Group(
                id=DefaultGroupId.MEMBERS,
                name=pgettext("default user group", "Members"),
                slug="members",
                is_hidden=True,
                is_default=True,
                ordering=2,
                # Permissions
                can_use_private_threads=True,
                can_start_private_threads=True,
                private_thread_users_limit=5,
                can_edit_own_threads=True,
                own_threads_edit_time_limit=0,
                can_edit_own_posts=True,
                own_posts_edit_time_limit=0,
                can_change_username=True,
                username_changes_limit=5,
                username_changes_expire=4,
                username_changes_span=1,
                can_see_user_profiles=True,
            ),
            Group(
                id=DefaultGroupId.GUESTS,
                name=pgettext("default user group", "Guests"),
                slug="guests",
                is_hidden=True,
                ordering=3,
                # Permissions
                can_see_user_profiles=True,
            ),
        ]
    )

    GroupDescription = apps.get_model("misago_users", "GroupDescription")
    GroupDescription.objects.bulk_create(
        [GroupDescription(group=group) for group in groups]
    )


def set_users_default_groups(apps, schema_editor):
    User = apps.get_model("misago_users", "User")

    # Put all staff users in admins group
    User.objects.filter(is_staff=True).update(
        group_id=DefaultGroupId.ADMINS,
        groups_ids=[DefaultGroupId.ADMINS],
        permissions_id=get_permissions_id([DefaultGroupId.ADMINS.value]),
    )

    # Set all superusers as root admins
    User.objects.filter(is_superuser=True).update(is_misago_root=True)

    # Put all non-staff users in members group
    User.objects.filter(is_staff=False).update(
        group_id=DefaultGroupId.MEMBERS,
        groups_ids=[DefaultGroupId.MEMBERS],
        permissions_id=get_permissions_id([DefaultGroupId.MEMBERS.value]),
    )


class Migration(migrations.Migration):
    dependencies = [
        ("misago_users", "0027_new_permissions"),
    ]

    operations = [
        migrations.RunPython(
            create_default_groups,
            migrations.RunPython.noop,
        ),
        migrations.RunPython(
            set_users_default_groups,
            migrations.RunPython.noop,
        ),
        migrations.RunSQL(
            f"ALTER SEQUENCE misago_users_group_id_seq RESTART WITH {CUSTOM_GROUP_ID_START};",
            migrations.RunSQL.noop,
        ),
    ]
