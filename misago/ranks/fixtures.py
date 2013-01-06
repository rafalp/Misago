from misago.ranks.models import Rank
from misago.utils import ugettext_lazy as _
from misago.utils import get_msgid

def load_fixtures():
    Rank.objects.create(
                        name=_("Forum Team").message,
                        name_slug='forum_team',
                        title=_("Forum Team").message,
                        style='rank-team',
                        special=True,
                        order=0,
                        as_tab=True,
                        on_index=True,
                        )
    
    Rank.objects.create(
                        name=_("Most Valuable Posters").message,
                        title=_("MVP").message,
                        style='rank-mvp',
                        special=True,
                        order=1,
                        as_tab=True,
                        )
    
    Rank.objects.create(
                        name=_("Lurkers").message,
                        order=1,
                        criteria="100%"
                        )
    
    Rank.objects.create(
                        name=_("Members").message,
                        order=2,
                        criteria="75%"
                        )
    
    Rank.objects.create(
                        name=_("Active Members").message,
                        style='rank-active',
                        order=3,
                        criteria="10%",
                        as_tab=True,
                        )