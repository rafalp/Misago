# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.translation import ugettext as _

from misago.core import serializer


def pickle_permissions(role, permissions):
    role.pickled_permissions = serializer.dumps(permissions)


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

            # threads perms
            'misago.threads.permissions': {
                'can_see_all_threads': 1,
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

            # threads perms
            'misago.threads.permissions': {
                'can_see_all_threads': 1,
                'can_reply_threads': 1,
                'can_edit_replies': 1,
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

            # threads perms
            'misago.threads.permissions': {
                'can_see_all_threads': 1,
                'can_start_threads': 1,
                'can_reply_threads': 1,
                'can_edit_threads': 1,
                'can_edit_replies': 1,
            },
        })
    standard.save()

    standard_with_polls = ForumRole(
        name=_('Start and reply threads, make polls'))
    pickle_permissions(standard_with_polls,
        {
            # forums perms
            'misago.forums.permissions': {
                'can_see': 1,
                'can_browse': 1,
            },

            # threads perms
            'misago.threads.permissions': {
                'can_see_all_threads': 1,
                'can_start_threads': 1,
                'can_reply_threads': 1,
                'can_edit_threads': 1,
                'can_edit_replies': 1,
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

            # threads perms
            'misago.threads.permissions': {
                'can_see_all_threads': 1,
                'can_start_threads': 1,
                'can_reply_threads': 2,
                'can_edit_threads': 2,
                'can_edit_replies': 2,
                'can_hide_own_threads': 2,
                'can_hide_own_replies': 2,
                'thread_edit_time': 0,
                'reply_edit_time': 0,
                'can_hide_threads': 2,
                'can_hide_replies': 2,
                'can_protect_posts': 1,
                'can_move_posts': 1,
                'can_merge_posts': 1,
                'can_change_threads_labels': 2,
                'can_pin_threads': 1,
                'can_close_threads': 1,
                'can_move_threads': 1,
                'can_merge_threads': 1,
                'can_review_moderated_content': 1,
                'can_report_content': 1,
                'can_see_reports': 1,
                'can_hide_events': 2,
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
