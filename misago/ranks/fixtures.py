from misago.ranks.models import Rank
from misago.utils import ugettext_lazy as _
from misago.utils import get_msgid

def load_fixtures():
    rank_staff = Rank(
                      name=_("Forum Team").message,
                      name_slug='forum_team',
                      title=_("Forum Team").message,
                      style='staff',
                      special=True,
                      order=0,
                      as_tab=True,
                      )
    rank_lurker = Rank(
                      name=_("Lurker").message,
                      style='lurker',
                      order=1,
                      criteria="100%"
                      )
    rank_member = Rank(
                      name=_("Member").message,
                      order=2,
                      criteria="75%"
                      )
    rank_active = Rank(
                      name=_("Most Valueable Posters").message,
                      title=_("MVP").message,
                      style='active',
                      order=3,
                      criteria="5%",
                      as_tab=True,
                      )
    
    rank_staff.save(force_insert=True)
    rank_lurker.save(force_insert=True)
    rank_member.save(force_insert=True)
    rank_active.save(force_insert=True)