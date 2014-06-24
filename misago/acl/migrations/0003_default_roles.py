# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.translation import ugettext as _
import base64
try:
    import cPickle as pickle
except ImportError:
    import pickle


def pickle_permissions(role, permissions):
    role.pickled_permissions = base64.encodestring(
        pickle.dumps(permissions, pickle.HIGHEST_PROTOCOL))


def create_default_roles(apps, schema_editor):
    Role = apps.get_model('misago_acl', 'Role')

    role = Role(name=_("Member"), special_role='authenticated')
    pickle_permissions(role,
        {
            # account perms
            'misago.users.permissions.account': {
                'name_changes_allowed': 2,
                'name_changes_expire': 180,
                'can_have_signature': False,
                'allow_signature_links': False,
                'allow_signature_images': False,
            },

            # profiles perms
            'misago.users.permissions.profiles': {
                'can_search_users': True,
                'can_see_users_emails': False,
                'can_see_users_ips': False,
                'can_see_hidden_users': False,
            },

            # destroy users perms
            'misago.users.permissions.destroying': {
                'can_destroy_user_newer_than': 0,
                'can_destroy_users_with_less_posts_than': 0,
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
                'can_have_signature': False,
                'allow_signature_links': False,
                'allow_signature_images': False,
            },

            # profiles perms
            'misago.users.permissions.profiles': {
                'can_search_users': True,
                'can_see_users_emails': False,
                'can_see_users_ips': False,
                'can_see_hidden_users': False,
            },

            # destroy users perms
            'misago.users.permissions.destroying': {
                'can_destroy_user_newer_than': 0,
                'can_destroy_users_with_less_posts_than': 0,
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
                'can_have_signature': True,
                'allow_signature_links': True,
                'allow_signature_images': False,
            },

            # profiles perms
            'misago.users.permissions.profiles': {
                'can_search_users': True,
                'can_see_users_emails': True,
                'can_see_users_ips': True,
                'can_see_hidden_users': True,
            },

            # destroy users perms
            'misago.users.permissions.destroying': {
                'can_destroy_user_newer_than': 0,
                'can_destroy_users_with_less_posts_than': 0,
            },
        })
    role.save()

    role = Role(name=_("Spam accounts destroyer"))
    pickle_permissions(role,
        {
            # destroy users perms
            'misago.users.permissions.destroying': {
                'can_destroy_user_newer_than': 2,
                'can_destroy_users_with_less_posts_than': 20,
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
