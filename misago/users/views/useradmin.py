from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from misago.admin.views import generic


class UserAdmin(generic.AdminBaseMixin):
    root_link = 'misago:admin:users:accounts:index'
    template_dir = 'misago/admin/users'

    def get_model(self):
        return get_user_model()


class UsersList(UserAdmin, generic.ItemsList):
    items_per_page = 20
    ordering = (
        (_("From newest"), '-joined_on'),
        (_("From oldest"), 'joined_on'),
        (_("A to z"), 'username'),
        (_("Z to a"), '-username'),
        )
