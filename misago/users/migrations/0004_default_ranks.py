from django.db import migrations

from ...core.utils import slugify

pgettext_lazy = lambda c, s: s


def create_default_ranks(apps, schema_editor):
    Rank = apps.get_model("misago_users", "Rank")

    team = Rank.objects.create(
        name=pgettext_lazy("rank name", "Forum team"),
        slug=slugify(pgettext_lazy("rank name", "Forum team")),
        title=pgettext_lazy("rank name", "Team"),
        css_class="primary",
        is_tab=True,
        order=0,
    )

    member = Rank.objects.create(
        name=pgettext_lazy("rank name", "Members"),
        slug=slugify(pgettext_lazy("rank name", "Members")),
        is_default=True,
        order=1,
    )

    Role = apps.get_model("misago_acl", "Role")

    team.roles.add(Role.objects.get(name=pgettext_lazy("role name", "Moderator")))
    team.roles.add(Role.objects.get(name=pgettext_lazy("role name", "Private threads")))
    team.roles.add(
        Role.objects.get(name=pgettext_lazy("role name", "Private threads moderator"))
    )
    team.roles.add(Role.objects.get(name=pgettext_lazy("role name", "Deleting users")))

    member.roles.add(
        Role.objects.get(name=pgettext_lazy("role name", "Private threads"))
    )


class Migration(migrations.Migration):
    dependencies = [
        ("misago_users", "0003_bans_version_tracker"),
        ("misago_acl", "0003_default_roles"),
    ]

    operations = [migrations.RunPython(create_default_ranks)]
