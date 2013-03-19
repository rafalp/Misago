from misago.models import Rank
from misago.utils.translation import ugettext_lazy as _

def load():
    Rank.objects.create(
                        name=_("Forum Team").message,
                        slug='forum-team',
                        title=_("Forum Team").message,
                        style='team',
                        special=True,
                        order=0,
                        as_tab=True,
                        on_index=True,
                        )

    Rank.objects.create(
                        name=_("Most Valuable Posters").message,
                        slug='most-valuable-posters',
                        title=_("MVP").message,
                        style='mvp',
                        special=True,
                        order=1,
                        as_tab=True,
                        )

    Rank.objects.create(
                        name=_("Top Posters").message,
                        slug='top-posters',
                        title="Top",
                        style='top',
                        order=2,
                        criteria="10%",
                        as_tab=True,
                        )

    Rank.objects.create(
                        name=_("Members").message,
                        slug='members',
                        order=4,
                        criteria="75%"
                        )

    Rank.objects.create(
                        name=_("Lurkers").message,
                        slug='lurkers',
                        order=5,
                        criteria="100%"
                        )