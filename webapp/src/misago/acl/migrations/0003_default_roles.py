from django.db import migrations

_ = lambda s: s


def create_default_roles(apps, schema_editor):
    Role = apps.get_model("misago_acl", "Role")

    Role.objects.create(
        name=_("Member"),
        special_role="authenticated",
        permissions={
            # account
            "misago.users.permissions.account": {
                "name_changes_allowed": 2,
                "name_changes_expire": 180,
                "can_have_signature": 0,
                "allow_signature_links": 0,
                "allow_signature_images": 0,
            },
            # profiles
            "misago.users.permissions.profiles": {
                "can_browse_users_list": 1,
                "can_search_users": 1,
                "can_follow_users": 1,
                "can_be_blocked": 1,
                "can_see_users_name_history": 0,
                "can_see_users_emails": 0,
                "can_see_users_ips": 0,
                "can_see_hidden_users": 0,
            },
            # attachments
            "misago.threads.permissions.attachments": {
                "max_attachment_size": 4 * 1024,
                "can_download_other_users_attachments": True,
            },
            # polls
            "misago.threads.permissions.polls": {
                "can_start_polls": 1,
                "can_edit_polls": 1,
            },
            # search
            "misago.search.permissions": {"can_search": 1},
        },
    )

    Role.objects.create(
        name=_("Guest"),
        special_role="anonymous",
        permissions={
            # account
            "misago.users.permissions.account": {
                "name_changes_allowed": 0,
                "name_changes_expire": 0,
                "can_have_signature": 0,
                "allow_signature_links": 0,
                "allow_signature_images": 0,
            },
            # profiles
            "misago.users.permissions.profiles": {
                "can_browse_users_list": 1,
                "can_search_users": 1,
                "can_see_users_name_history": 0,
                "can_see_users_emails": 0,
                "can_see_users_ips": 0,
                "can_see_hidden_users": 0,
            },
            # attachments
            "misago.threads.permissions.attachments": {
                "can_download_other_users_attachments": True
            },
            # search
            "misago.search.permissions": {"can_search": 1},
        },
    )

    Role.objects.create(
        name=_("Moderator"),
        permissions={
            # account
            "misago.users.permissions.account": {
                "name_changes_allowed": 5,
                "name_changes_expire": 14,
                "can_have_signature": 1,
                "allow_signature_links": 1,
                "allow_signature_images": 0,
            },
            # profiles
            "misago.users.permissions.profiles": {
                "can_browse_users_list": 1,
                "can_search_users": 1,
                "can_be_blocked": 0,
                "can_see_users_name_history": 1,
                "can_see_ban_details": 1,
                "can_see_users_emails": 1,
                "can_see_users_ips": 1,
                "can_see_hidden_users": 1,
            },
            # attachments
            "misago.threads.permissions.attachments": {
                "max_attachment_size": 8 * 1024,
                "can_download_other_users_attachments": True,
                "can_delete_other_users_attachments": True,
            },
            # polls
            "misago.threads.permissions.polls": {
                "can_start_polls": 2,
                "can_edit_polls": 2,
                "can_delete_polls": 2,
                "can_always_see_poll_voters": 1,
            },
            # moderation
            "misago.threads.permissions.threads": {
                "can_see_unapproved_content_lists": True,
                "can_see_reported_content_lists": True,
                "can_omit_flood_protection": True,
            },
            "misago.users.permissions.moderation": {
                "can_warn_users": 1,
                "can_moderate_avatars": 1,
                "can_moderate_signatures": 1,
                "can_moderate_profile_details": 1,
            },
            # delete users
            "misago.users.permissions.delete": {
                "can_delete_users_newer_than": 0,
                "can_delete_users_with_less_posts_than": 0,
            },
        },
    )

    Role.objects.create(
        name=_("Renaming users"),
        permissions={
            # rename users
            "misago.users.permissions.moderation": {"can_rename_users": 1}
        },
    )

    Role.objects.create(
        name=_("Banning users"),
        permissions={
            # ban users
            "misago.users.permissions.profiles": {"can_see_ban_details": 1},
            "misago.users.permissions.moderation": {
                "can_ban_users": 1,
                "max_ban_length": 14,
                "can_lift_bans": 1,
                "max_lifted_ban_length": 14,
            },
        },
    )

    Role.objects.create(
        name=_("Deleting users"),
        permissions={
            # delete users
            "misago.users.permissions.delete": {
                "can_delete_users_newer_than": 3,
                "can_delete_users_with_less_posts_than": 7,
            }
        },
    )

    Role.objects.create(
        name=_("Can't be blocked"),
        permissions={
            # profiles
            "misago.users.permissions.profiles": {"can_be_blocked": 0}
        },
    )

    Role.objects.create(
        name=_("Private threads"),
        permissions={
            # private threads
            "misago.threads.permissions.privatethreads": {
                "can_use_private_threads": 1,
                "can_start_private_threads": 1,
                "max_private_thread_participants": 3,
                "can_add_everyone_to_private_threads": 0,
                "can_report_private_threads": 1,
                "can_moderate_private_threads": 0,
            }
        },
    )

    Role.objects.create(
        name=_("Private threads moderator"),
        permissions={
            # private threads
            "misago.threads.permissions.privatethreads": {
                "can_use_private_threads": 1,
                "can_start_private_threads": 1,
                "max_private_thread_participants": 15,
                "can_add_everyone_to_private_threads": 1,
                "can_report_private_threads": 1,
                "can_moderate_private_threads": 1,
            }
        },
    )


class Migration(migrations.Migration):

    dependencies = [("misago_acl", "0002_acl_version_tracker")]

    operations = [migrations.RunPython(create_default_roles)]
