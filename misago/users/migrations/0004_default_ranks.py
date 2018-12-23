from django.db import migrations
from django.utils.translation import gettext

from ...core.utils import slugify

_ = lambda s: s


def create_default_ranks(apps, schema_editor):
    Rank = apps.get_model("misago_users", "Rank")

    team = Rank.objects.create(
        name=gettext("Forum team"),
        slug=slugify(gettext("Forum team")),
        title=gettext("Team"),
        css_class="primary",
        is_tab=True,
        order=0,
    )

    member = Rank.objects.create(
        name=gettext("Members"),
        slug=slugify(gettext("Members")),
        is_default=True,
        order=1,
    )

    Role = apps.get_model("misago_acl", "Role")

    team.roles.add(Role.objects.get(name=_("Moderator")))
    team.roles.add(Role.objects.get(name=_("Private threads")))
    team.roles.add(Role.objects.get(name=_("Private threads moderator")))
    team.roles.add(Role.objects.get(name=_("Deleting users")))

    member.roles.add(Role.objects.get(name=_("Private threads")))


class Migration(migrations.Migration):

    dependencies = [
        ("misago_users", "0003_bans_version_tracker"),
        ("misago_acl", "0003_default_roles"),
    ]

    operations = [migrations.RunPython(create_default_ranks)]
