from django.utils.translation import ugettext_lazy as _
from misago.admin.views import generic
from misago.users.models import Rank


class RankAdmin(generic.AdminBaseMixin):
    root_link = 'misago:admin:users:ranks:index'
    template_dir = 'misago/admin/ranks'

    def get_model(self):
        return Rank


class RanksList(RankAdmin, generic.ItemsList):
    ordering = ((None, 'order'),)
