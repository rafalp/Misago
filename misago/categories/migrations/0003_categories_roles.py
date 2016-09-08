# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.utils.translation import ugettext as _

from misago.core import serializer


def pickle_permissions(role, permissions):
    role.pickled_permissions = serializer.dumps(permissions)


def create_default_categories_roles(apps, schema_editor):
    """
    Crete roles
    """
    CategoryRole = apps.get_model('misago_categories', 'CategoryRole')

    see_only = CategoryRole(name=_('See only'))
    pickle_permissions(see_only,
        {
            # categories perms
            'misago.categories.permissions': {
                'can_see': 1,
                'can_browse': 0
            },
        })
    see_only.save()

    read_only = CategoryRole(name=_('Read only'))
    pickle_permissions(read_only,
        {
            # categories perms
            'misago.categories.permissions': {
                'can_see': 1,
                'can_browse': 1
            },

            # threads perms
            'misago.threads.permissions.threads': {
                'can_see_all_threads': 1,
                'can_see_posts_likes': 2,
                'can_download_other_users_attachments': 1,
                'can_like_posts': 1
            },
        })
    read_only.save()

    reply_only = CategoryRole(name=_('Reply to threads'))
    pickle_permissions(reply_only,
        {
            # categories perms
            'misago.categories.permissions': {
                'can_see': 1,
                'can_browse': 1
            },

            # threads perms
            'misago.threads.permissions.threads': {
                'can_see_all_threads': 1,
                'can_reply_threads': 1,
                'can_edit_posts': 1,
                'can_download_other_users_attachments': 1,
                'max_attachment_size': 500,
                'can_see_posts_likes': 2,
                'can_like_posts': 1
            },
        })
    reply_only.save()

    standard = CategoryRole(name=_('Start and reply threads'))
    pickle_permissions(standard,
        {
            # categories perms
            'misago.categories.permissions': {
                'can_see': 1,
                'can_browse': 1
            },

            # threads perms
            'misago.threads.permissions.threads': {
                'can_see_all_threads': 1,
                'can_start_threads': 1,
                'can_reply_threads': 1,
                'can_edit_threads': 1,
                'can_edit_posts': 1,
                'can_download_other_users_attachments': 1,
                'max_attachment_size': 500,
                'can_see_posts_likes': 2,
                'can_like_posts': 1
            },
        })
    standard.save()

    standard_with_polls = CategoryRole(name=_('Start and reply threads, make polls'))
    pickle_permissions(standard_with_polls,
        {
            # categories perms
            'misago.categories.permissions': {
                'can_see': 1,
                'can_browse': 1,
            },

            # threads perms
            'misago.threads.permissions.threads': {
                'can_see_all_threads': 1,
                'can_start_threads': 1,
                'can_reply_threads': 1,
                'can_edit_threads': 1,
                'can_edit_posts': 1,
                'can_download_other_users_attachments': 1,
                'max_attachment_size': 500,
                'can_see_posts_likes': 2,
                'can_like_posts': 1
            },
        })
    standard_with_polls.save()

    moderator = CategoryRole(name=_('Moderator'))
    pickle_permissions(moderator,
        {
            # categories perms
            'misago.categories.permissions': {
                'can_see': 1,
                'can_browse': 1
            },

            # threads perms
            'misago.threads.permissions.threads': {
                'can_see_all_threads': 1,
                'can_start_threads': 1,
                'can_reply_threads': 1,
                'can_edit_threads': 2,
                'can_edit_posts': 2,
                'can_hide_own_threads': 2,
                'can_hide_own_posts': 2,
                'thread_edit_time': 0,
                'post_edit_time': 0,
                'can_hide_threads': 2,
                'can_hide_posts': 2,
                'can_protect_posts': 1,
                'can_move_posts': 1,
                'can_merge_posts': 1,
                'can_announce_threads': 1,
                'can_pin_threads': 2,
                'can_close_threads': 1,
                'can_move_threads': 1,
                'can_merge_threads': 1,
                'can_approve_content': 1,
                'can_download_other_users_attachments': 1,
                'max_attachment_size': 2500,
                'can_delete_other_users_attachments': 1,
                'can_see_posts_likes': 2,
                'can_like_posts': 1,
                'can_report_content': 1,
                'can_see_reports': 1,
                'can_hide_events': 2
            },
        })
    moderator.save()

    """
    Assign category roles to roles
    """
    Category = apps.get_model('misago_categories', 'Category')
    Role = apps.get_model('misago_acl', 'Role')
    RoleCategoryACL = apps.get_model('misago_categories', 'RoleCategoryACL')

    moderators = Role.objects.get(name=_('Moderator'))
    members = Role.objects.get(special_role='authenticated')
    guests = Role.objects.get(special_role='anonymous')

    category = Category.objects.get(tree_id=1, level=1)

    RoleCategoryACL.objects.bulk_create([
        RoleCategoryACL(
            role=moderators,
            category=category,
            category_role=moderator
        ),

        RoleCategoryACL(
            role=members,
            category=category,
            category_role=standard
        ),

        RoleCategoryACL(
            role=guests,
            category=category,
            category_role=read_only
        ),
    ])


class Migration(migrations.Migration):

    dependencies = [
        ('misago_categories', '0002_default_categories'),
        ('misago_acl', '0003_default_roles'),
    ]

    operations = [
        migrations.RunPython(create_default_categories_roles),
    ]
