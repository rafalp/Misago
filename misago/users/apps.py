from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _
from misago.users.pages import usercp, users_list, user_profile


class MisagoUsersConfig(AppConfig):
    name = 'misago.users'
    label = 'misago_users'
    verbose_name = "Misago Auth"

    def ready(self):
        from misago.users import signals

        self.register_default_usercp_pages()
        self.register_default_users_list_pages()
        self.register_default_user_profile_pages()

    def register_default_usercp_pages(self):
        def show_signature_cp(request):
            return request.user.acl['can_have_signature']

        usercp.add_section(
            link='misago:usercp_change_forum_options',
            name=_('Forum options'),
            component='forum-options',
            icon='settings')

        usercp.add_section(
            link='misago:usercp_change_username',
            name=_('Change username'),
            component='change-username',
            icon='card_membership')

        usercp.add_section(
            link='misago:usercp_change_email_password',
            name=_('Change email or password'),
            component='sign-in-credentials',
            icon='vpn_key')

    def register_default_users_list_pages(self):
        users_list.add_section(
            link='misago:users_active_posters',
            component='active-posters',
            name=_('Active posters'))

    def register_default_user_profile_pages(self):
        def posts_badge(request, profile):
            return {
                'value': profile.posts,
                'attr': 'posts',
            }

        def threads_badge(request, profile):
            return {
                'value': profile.threads,
                'attr': 'threads',
            }

        def followers_badge(request, profile):
            return {
                'value': profile.followers,
                'attr': 'followers',
            }

        def following_badge(request, profile):
            return {
                'value': profile.following,
                'attr': 'following',
            }

        def can_see_names_history(request, profile):
            if request.user.is_authenticated():
                is_account_owner = profile.pk == request.user.pk
                has_permission = request.user.acl['can_see_users_name_history']
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

        user_profile.add_section(
            link='misago:user_posts',
            name=_("Posts"),
            icon='message',
            component='posts',
            get_metadata=posts_badge)

        user_profile.add_section(
            link='misago:user_threads',
            name=_("Threads"),
            icon='forum',
            component='threads',
            get_metadata=threads_badge)

        user_profile.add_section(
            link='misago:user_followers',
            name=_("Followers"),
            icon='favorite',
            component='followers',
            get_metadata=followers_badge)

        user_profile.add_section(
            link='misago:user_follows',
            name=_("Follows"),
            icon='favorite_border',
            component='follows',
            get_metadata=following_badge)

        user_profile.add_section(
            link='misago:username_history',
            name=_("Username history"),
            icon='card_membership',
            component='username-history',
            visible_if=can_see_names_history)

        user_profile.add_section(
            link='misago:user_ban',
            name=_("Ban details"),
            icon='remove_circle_outline',
            component='ban-details',
            visible_if=can_see_ban_details)

