# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.translation import ugettext as _

from misago.core import serializer


def pickle_permissions(role, permissions):
    role.pickled_permissions = serializer.dumps(permissions)


def create_default_roles(apps, schema_editor):
    Role = apps.get_model('misago_acl', 'Role')

    role = Role(name=_("Member"), special_role='authenticated')
    pickle_permissions(role,
        {
            # account perms
            'misago.users.permissions.account': {
                'name_changes_allowed': 2,
                'name_changes_expire': 180,
                'can_have_signature': 0,
                'allow_signature_links': 0,
                'allow_signature_images': 0,
            },

            # profiles perms
            'misago.users.permissions.profiles': {
                'can_browse_users_list': 1,
                'can_see_users_online_list': 0,
                'can_search_users': 1,
                'can_follow_users': 1,
                'can_be_blocked': 1,
                'can_see_users_name_history': 0,
                'can_see_users_emails': 0,
                'can_see_users_ips': 0,
                'can_see_hidden_users': 0,
            },

            # delete users perms
            'misago.users.permissions.delete': {
                'can_delete_users_newer_than': 0,
                'can_delete_users_with_less_posts_than': 0,
            },
        })
    role.save()

    role = Role(name=_("Guest"), special_role='anonymous')
    pickle_permissions(role,
        {
            # account perms
            'misago.users.permissions.account': {
                'name_changes_allowed': 0,
                'name_changes_expire': 0,
                'can_have_signature': 0,
                'allow_signature_links': 0,
                'allow_signature_images': 0,
            },

            # profiles perms
            'misago.users.permissions.profiles': {
                'can_browse_users_list': 1,
                'can_see_users_online_list': 0,
                'can_search_users': 1,
                'can_see_users_name_history': 0,
                'can_see_users_emails': 0,
                'can_see_users_ips': 0,
                'can_see_hidden_users': 0,
            },

            # delete users perms
            'misago.users.permissions.delete': {
                'can_delete_users_newer_than': 0,
                'can_delete_users_with_less_posts_than': 0,
            },
        })
    role.save()

    role = Role(name=_("Moderator"))
    pickle_permissions(role,
        {
            # account perms
            'misago.users.permissions.account': {
                'name_changes_allowed': 5,
                'name_changes_expire': 14,
                'can_have_signature': 1,
                'allow_signature_links': 1,
                'allow_signature_images': 0,
            },

            # profiles perms
            'misago.users.permissions.profiles': {
                'can_browse_users_list': 1,
                'can_see_users_online_list': 1,
                'can_search_users': 1,
                'can_be_blocked': 0,
                'can_see_users_name_history': 1,
                'can_see_ban_details': 1,
                'can_see_users_emails': 1,
                'can_see_users_ips': 1,
                'can_see_hidden_users': 1,
            },

            # warnings perms
            'misago.users.permissions.warnings': {
                'can_see_other_users_warnings': 1,
                'can_warn_users': 1,
                'can_cancel_warnings': 1,
                'can_be_warned': 0,
            },

            # moderation perms
            'misago.users.permissions.moderation': {
                'can_warn_users': 1,
                'can_moderate_avatars': 1,
                'can_moderate_signatures': 1,
            },

            # delete users perms
            'misago.users.permissions.delete': {
                'can_delete_users_newer_than': 0,
                'can_delete_users_with_less_posts_than': 0,
            },
        })
    role.save()

    role = Role(name=_("See warnings"))
    pickle_permissions(role,
        {
            # warnings perms
            'misago.users.permissions.warnings': {
                'can_see_other_users_warnings': 1,
            },
        })
    role.save()

    role = Role(name=_("Renaming users"))
    pickle_permissions(role,
        {
            # rename users perms
            'misago.users.permissions.moderation': {
                'can_rename_users': 1,
            },
        })
    role.save()

    role = Role(name=_("Banning users"))
    pickle_permissions(role,
        {
            # ban users perms
            'misago.users.permissions.profiles': {
                'can_see_ban_details': 1,
            },

            'misago.users.permissions.moderation': {
                'can_ban_users': 1,
                'max_ban_length': 14,
                'can_lift_bans': 1,
                'max_lifted_ban_length': 14,
            },
        })

    role.save()
    role = Role(name=_("Deleting users"))
    pickle_permissions(role,
        {
            # delete users perms
            'misago.users.permissions.delete': {
                'can_delete_users_newer_than': 3,
                'can_delete_users_with_less_posts_than': 7,
            },
        })
    role.save()

    role = Role(name=_("Can't be blocked"))
    pickle_permissions(role,
        {
            # profiles perms
            'misago.users.permissions.profiles': {
                'can_be_blocked': 0,
            },
        })
    role.save()


class Migration(migrations.Migration):

    dependencies = [
        ('misago_acl', '0002_acl_version_tracker'),
    ]

    operations = [
        migrations.RunPython(create_default_roles),
    ]
