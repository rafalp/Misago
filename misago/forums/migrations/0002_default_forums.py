# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.translation import ugettext as _

from misago.core.utils import slugify


def create_default_forums_tree(apps, schema_editor):
    Forum = apps.get_model('misago_forums', 'Forum')

    Forum.objects.create(
        special_role='private_threads',
        role='forum',
        name='Private',
        slug='private',
        lft=1,
        rght=2,
        tree_id=0,
        level=0,
    )

    root = Forum.objects.create(
        special_role='root_category',
        role='category',
        name='Root',
        slug='root',
        lft=3,
        rght=10,
        tree_id=1,
        level=0,
    )

    category_name = _("First category")
    forum_name = _("First forum")
    redirect_name = _("Misago support forums")
    redirect_link = _("http://misago-project.org")

    category = Forum.objects.create(
        parent=root,
        lft=4,
        rght=9,
        tree_id=1,
        level=1,
        role='category',
        name=category_name,
        slug=slugify(category_name))

    Forum.objects.create(
        parent=category,
        lft=5,
        rght=6,
        tree_id=1,
        level=2,
        role='forum',
        name=forum_name,
        slug=slugify(forum_name))

    Forum.objects.create(
        parent=category,
        lft=7,
        rght=8,
        tree_id=1,
        level=2,
        role='redirect',
        name=redirect_name,
        slug=slugify(redirect_name),
        redirect_url=redirect_link)


class Migration(migrations.Migration):

    dependencies = [
        ('misago_forums', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_default_forums_tree),
    ]
