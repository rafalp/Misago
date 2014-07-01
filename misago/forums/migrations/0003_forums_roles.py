# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import base64
try:
    import cPickle as pickle
except ImportError:
    import pickle

from django.db import models, migrations
from django.utils.translation import ugettext as _

def pickle_permissions(role, permissions):
    role.pickled_permissions = base64.encodestring(
        pickle.dumps(permissions, pickle.HIGHEST_PROTOCOL))


def create_default_forums_roles(apps, schema_editor):
    """
    Crete roles
    """
    ForumRole = apps.get_model('misago_forums', 'ForumRole')

    see_only = ForumRole(name=_('See only'))
    pickle_permissions(see_only,
        {
            # forums perms
            'misago.forums.permissions': {
                'can_see': 1,
                'can_browse': 0,
            },
        })
    see_only.save()

    read_only = ForumRole(name=_('Read only'))
    pickle_permissions(read_only,
        {
            # forums perms
            'misago.forums.permissions': {
                'can_see': 1,
                'can_browse': 1,
            },
        })
    read_only.save()

    reply_only = ForumRole(name=_('Reply to threads'))
    pickle_permissions(reply_only,
        {
            # forums perms
            'misago.forums.permissions': {
                'can_see': 1,
                'can_browse': 1,
            },
        })
    reply_only.save()

    standard = ForumRole(name=_('Start and reply threads'))
    pickle_permissions(standard,
        {
            # forums perms
            'misago.forums.permissions': {
                'can_see': 1,
                'can_browse': 1,
            },
        })
    standard.save()

    standard_with_polls = ForumRole(
        name=_('Start and reply threads, make pols'))
    pickle_permissions(standard_with_polls,
        {
            # forums perms
            'misago.forums.permissions': {
                'can_see': 1,
                'can_browse': 1,
            },
        })
    standard_with_polls.save()

    moderator = ForumRole(name=_('Moderator'))
    pickle_permissions(moderator,
        {
            # forums perms
            'misago.forums.permissions': {
                'can_see': 1,
                'can_browse': 1,
            },
        })
    moderator.save()

    """
    Assign forum roles to roles
    """
    Forum = apps.get_model('misago_forums', 'Forum')
    Role = apps.get_model('misago_acl', 'Role')
    RoleForumACL = apps.get_model('misago_forums', 'RoleForumACL')

    moderators = Role.objects.get(name=_('Moderator'))
    members = Role.objects.get(special_role='authenticated')
    guests = Role.objects.get(special_role='anonymous')

    category = Forum.objects.filter(level__gt=0).get(role='category')
    forum = Forum.objects.filter(level__gt=0).get(role='forum')
    redirect = Forum.objects.filter(level__gt=0).get(role='redirect')

    RoleForumACL.objects.bulk_create([
        RoleForumACL(role=moderators, forum=category, forum_role=moderator),
        RoleForumACL(role=moderators, forum=forum, forum_role=moderator),
        RoleForumACL(role=moderators, forum=redirect, forum_role=moderator),

        RoleForumACL(role=members, forum=category, forum_role=standard),
        RoleForumACL(role=members, forum=forum, forum_role=standard),
        RoleForumACL(role=members, forum=redirect, forum_role=standard),

        RoleForumACL(role=guests, forum=category, forum_role=read_only),
        RoleForumACL(role=guests, forum=forum, forum_role=read_only),
        RoleForumACL(role=guests, forum=redirect, forum_role=read_only),
    ])


class Migration(migrations.Migration):

    dependencies = [
        ('misago_forums', '0002_default_forums'),
        ('misago_acl', '0003_default_roles'),
    ]

    operations = [
        migrations.RunPython(create_default_forums_roles),
    ]
