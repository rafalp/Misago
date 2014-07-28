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
        def show_signature_cp(request):
            return request.user.acl['can_have_signature']

        usercp.add_page(link='misago:usercp_change_forum_options',
                        name=_('Change forum options'),
                        icon='fa fa-check-square-o')
        usercp.add_page(link='misago:usercp_change_avatar',
                        name=_('Change avatar'),
                        icon='fa fa-image')
        usercp.add_page(link='misago:usercp_edit_signature',
                        name=_('Edit your signature'),
                        icon='fa fa-pencil',
                        visibility_condition=show_signature_cp)
        usercp.add_page(link='misago:usercp_change_username',
                        name=_('Change username'),
                        icon='fa fa-credit-card')
        usercp.add_page(link='misago:usercp_change_email_password',
                        name=_('Change email or password'),
                        icon='fa fa-ticket')

    def register_default_users_list_pages(self):
        users_list.add_page(link='misago:index',
                            name='Todo',
                            icon='fa fa-check')

    def register_default_user_profile_pages(self):
        user_profile.add_page(link='misago:user_posts',
                              name=_("Posts"))
        user_profile.add_page(link='misago:user_threads',
                              name=_("Threads"))
