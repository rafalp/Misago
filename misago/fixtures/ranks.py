from misago.models import Rank
from misago.utils.translation import ugettext_lazy as _

def load():
    Rank.objects.create(
                        name=_("Forum Team").message,
                        name_slug='forum-team',
                        title=_("Forum Team").message,
                        style='team',
                        special=True,
                        order=0,
                        as_tab=True,
                        on_index=True,
                        )

    Rank.objects.create(
                        name=_("Most Valuable Posters").message,
                        name_slug='most-valuable-posters',
                        title=_("MVP").message,
                        style='mvp',
                        special=True,
                        order=1,
                        as_tab=True,
                        )

    Rank.objects.create(
                        name=_("Lurkers").message,
                        name_slug='lurkers',
                        order=1,
                        criteria="100%"
                        )

    Rank.objects.create(
                        name=_("Members").message,
                        name_slug='members',
                        order=2,
                        criteria="75%"
                        )

    Rank.objects.create(
                        name=_("Active Members").message,
                        name_slug='active-members',
                        style='active',
                        order=3,
                        criteria="10%",
                        as_tab=True,
                        )