from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from misago.admin.views import generic


class UserAdmin(generic.AdminBaseMixin):
    root_link = 'misago:admin:users:accounts:index'
    templates_dir = 'misago/admin/users'

    def get_model(self):
        return get_user_model()


class UsersList(UserAdmin, generic.ListView):
    items_per_page = 20
    ordering = (
        ('-id', _("From newest")),
        ('id', _("From oldest")),
        ('username', _("A to z")),
        ('-username', _("Z to a")),
        )
