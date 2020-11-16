from django.db import migrations

_ = lambda s: s


def create_default_categories_roles(apps, schema_editor):
    CategoryRole = apps.get_model("misago_categories", "CategoryRole")

    CategoryRole.objects.create(
        name=_("See only"),
        permissions={
            # categories perms
            "misago.categories.permissions": {"can_see": 1, "can_browse": 0}
        },
    )

    read_only = CategoryRole.objects.create(
        name=_("Read only"),
        permissions={
            # categories perms
            "misago.categories.permissions": {"can_see": 1, "can_browse": 1},
            # threads perms
            "misago.threads.permissions.threads": {
                "can_see_all_threads": 1,
                "can_see_posts_likes": 1,
                "can_download_other_users_attachments": 1,
                "can_like_posts": 1,
            },
        },
    )

    CategoryRole.objects.create(
        name=_("Reply to threads"),
        permissions={
            # categories perms
            "misago.categories.permissions": {"can_see": 1, "can_browse": 1},
            # threads perms
            "misago.threads.permissions.threads": {
                "can_see_all_threads": 1,
                "can_reply_threads": 1,
                "can_edit_posts": 1,
                "can_download_other_users_attachments": 1,
                "max_attachment_size": 500,
                "can_see_posts_likes": 2,
                "can_like_posts": 1,
            },
        },
    )

    standard = CategoryRole.objects.create(
        name=_("Start and reply threads"),
        permissions={
            # categories perms
            "misago.categories.permissions": {"can_see": 1, "can_browse": 1},
            # threads perms
            "misago.threads.permissions.threads": {
                "can_see_all_threads": 1,
                "can_start_threads": 1,
                "can_reply_threads": 1,
                "can_edit_threads": 1,
                "can_edit_posts": 1,
                "can_download_other_users_attachments": 1,
                "max_attachment_size": 500,
                "can_see_posts_likes": 2,
                "can_like_posts": 1,
            },
        },
    )

    moderator = CategoryRole.objects.create(
        name=_("Moderator"),
        permissions={
            # categories perms
            "misago.categories.permissions": {"can_see": 1, "can_browse": 1},
            # threads perms
            "misago.threads.permissions.threads": {
                "can_see_all_threads": 1,
                "can_start_threads": 1,
                "can_reply_threads": 1,
                "can_edit_threads": 2,
                "can_edit_posts": 2,
                "can_hide_own_threads": 2,
                "can_hide_own_posts": 2,
                "thread_edit_time": 0,
                "post_edit_time": 0,
                "can_hide_threads": 2,
                "can_hide_posts": 2,
                "can_protect_posts": 1,
                "can_move_posts": 1,
                "can_merge_posts": 1,
                "can_announce_threads": 1,
                "can_pin_threads": 2,
                "can_close_threads": 1,
                "can_move_threads": 1,
                "can_merge_threads": 1,
                "can_approve_content": 1,
                "can_download_other_users_attachments": 1,
                "max_attachment_size": 2500,
                "can_delete_other_users_attachments": 1,
                "can_see_posts_likes": 2,
                "can_like_posts": 1,
                "can_report_content": 1,
                "can_see_reports": 1,
                "can_hide_events": 2,
            },
        },
    )

    # assign category roles to roles
    Category = apps.get_model("misago_categories", "Category")
    Role = apps.get_model("misago_acl", "Role")
    RoleCategoryACL = apps.get_model("misago_categories", "RoleCategoryACL")

    category = Category.objects.get(tree_id=1, level=1)

    RoleCategoryACL.objects.create(
        role=Role.objects.get(name=_("Moderator")),
        category=category,
        category_role=moderator,
    )

    RoleCategoryACL.objects.create(
        role=Role.objects.get(special_role="authenticated"),
        category=category,
        category_role=standard,
    )

    RoleCategoryACL.objects.create(
        role=Role.objects.get(special_role="anonymous"),
        category=category,
        category_role=read_only,
    )


class Migration(migrations.Migration):

    dependencies = [
        ("misago_categories", "0002_default_categories"),
        ("misago_acl", "0003_default_roles"),
    ]

    operations = [migrations.RunPython(create_default_categories_roles)]
