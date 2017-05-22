# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations
from django.utils.translation import ugettext

from misago.core.utils import slugify


_ = lambda x: x


def create_default_ranks(apps, schema_editor):
    Rank = apps.get_model('misago_users', 'Rank')

    team = Rank.objects.create(
        name=ugettext("Forum team"),
        slug=slugify(ugettext("Forum team")),
        title=ugettext("Team"),
        css_class='primary',
        is_tab=True,
        order=0,
    )

    member = Rank.objects.create(
        name=ugettext("Members"),
        slug=slugify(ugettext("Members")),
        is_default=True,
        order=1,
    )

    Role = apps.get_model('misago_acl', 'Role')

    team.roles.add(Role.objects.get(name=_("Moderator")))
    team.roles.add(Role.objects.get(name=_("Private threads")))
    team.roles.add(Role.objects.get(name=_("Private threads moderator")))
    team.roles.add(Role.objects.get(name=_("Deleting users")))

    member.roles.add(Role.objects.get(name=_("Private threads")))


class Migration(migrations.Migration):

    dependencies = [
        ('misago_users', '0003_bans_version_tracker'),
        ('misago_acl', '0003_default_roles'),
    ]

    operations = [
        migrations.RunPython(create_default_ranks),
    ]
