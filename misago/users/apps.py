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
                        visible_if=show_signature_cp)
        usercp.add_page(link='misago:usercp_change_username',
                        name=_('Change username'),
                        icon='fa fa-credit-card')
        usercp.add_page(link='misago:usercp_change_email_password',
                        name=_('Change email or password'),
                        icon='fa fa-ticket')

    def register_default_users_list_pages(self):
        def can_see_online_list(request):
            return request.user.acl['can_see_users_online_list']
        users_list.add_page(link='misago:users_active_posters',
                            name=_('Active posters'))
        users_list.add_page(link='misago:users_online',
                            name=_('Online'),
                            visible_if=can_see_online_list)

    def register_default_user_profile_pages(self):
        def posts_badge(request, profile):
            return profile.posts
        def threads_badge(request, profile):
            return profile.threads
        def followers_badge(request, profile):
            return profile.followers
        def following_badge(request, profile):
            return profile.following
        def can_see_names_history(request, profile):
            if request.user.is_authenticated():
                is_account_owner = profile.pk == request.user.pk
                has_permission = request.user.acl['can_see_users_name_history']
                return is_account_owner or has_permission
            else:
                return False
        def can_see_warnings(request, profile):
            if request.user.is_authenticated():
                is_account_owner = profile.pk == request.user.pk
                user_acl = request.user.acl
                has_permission = user_acl['can_see_other_users_warnings']
                return is_account_owner or has_permission
            else:
                return False
        def can_see_ban_details(request, profile):
            if request.user.is_authenticated():
                if request.user.acl['can_see_ban_details']:
                    from misago.users.bans import get_user_ban
                    return bool(get_user_ban(profile))
                else:
                    return False
            else:
                return False

        user_profile.add_page(link='misago:user_posts',
                              name=_("Posts"),
                              badge=posts_badge)
        user_profile.add_page(link='misago:user_threads',
                              name=_("Threads"),
                              badge=threads_badge)
        user_profile.add_page(link='misago:user_followers',
                              name=_("Followers"),
                              badge=followers_badge)
        user_profile.add_page(link='misago:user_follows',
                              name=_("Follows"),
                              badge=following_badge)
        user_profile.add_page(link='misago:user_name_history',
                              name=_("Name history"),
                              visible_if=can_see_names_history)
        user_profile.add_page(link='misago:user_warnings',
                              name=_("Warnings"),
                              visible_if=can_see_warnings)
        user_profile.add_page(link='misago:user_ban',
                              name=_("Ban"),
                              visible_if=can_see_ban_details)
