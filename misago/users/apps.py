from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _
from misago.users.sites import usercp, users_list, user_profile


class MisagoUsersConfig(AppConfig):
    name = 'misago.users'
    label = 'misago_users'
    verbose_name = "Misago Auth"

    def ready(self):
        self.register_default_usercp_pages()
        self.register_default_users_list_pages()
        self.register_default_user_profile_pages()

    def register_default_usercp_pages(self):
        usercp.add_page(link='misago:index',
                        name='Not',
                        icon='fa fa-check')

    def register_default_users_list_pages(self):
        users_list.add_page(link='misago:index',
                            name='Todo',
                            icon='fa fa-check')

    def register_default_user_profile_pages(self):
        user_profile.add_page(link='misago:index',
                              name='Todo',
                              icon='fa fa-check')
