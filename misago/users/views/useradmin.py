from django.contrib.auth import get_user_model
from misago.admin.views import generic


class UserAdmin(generic.AdminBaseMixin):
    template_dir = 'misago/admin/users'

    def get_model(self):
        return get_user_model()


class UsersList(UserAdmin, generic.ItemsList):
    pass
