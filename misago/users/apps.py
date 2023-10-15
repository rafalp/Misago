from django.apps import AppConfig
from django.utils.translation import pgettext_lazy

from .pages import user_profile, usercp, users_list


class MisagoUsersConfig(AppConfig):
    name = "misago.users"
    label = "misago_users"
    verbose_name = "Misago Auth"

    def ready(self):
        from . import signals as _
        from .admin import tasks  # pylint: disable=unused-import

        self.register_default_usercp_pages()
        self.register_default_users_list_pages()
        self.register_default_user_profile_pages()

    def register_default_usercp_pages(self):
        def auth_is_not_delegated(request):
            return not request.settings.enable_oauth2_client

        usercp.add_section(
            link="misago:usercp-change-forum-options",
            name=pgettext_lazy("user options page", "Forum options"),
            component="forum-options",
            icon="settings",
        )
        usercp.add_section(
            link="misago:usercp-edit-details",
            name=pgettext_lazy("user options page", "Edit details"),
            component="edit-details",
            icon="person_outline",
        )
        usercp.add_section(
            link="misago:usercp-change-username",
            name=pgettext_lazy("user options page", "Change username"),
            component="change-username",
            icon="card_membership",
            visible_if=auth_is_not_delegated,
        )
        usercp.add_section(
            link="misago:usercp-change-email-password",
            name=pgettext_lazy("user options page", "Change e-mail or password"),
            component="sign-in-credentials",
            icon="vpn_key",
            visible_if=auth_is_not_delegated,
        )

        def can_download_own_data(request):
            return request.settings.allow_data_downloads

        usercp.add_section(
            link="misago:usercp-download-data",
            name=pgettext_lazy("user options page", "Download data"),
            component="download-data",
            icon="save_alt",
            visible_if=can_download_own_data,
        )

        def can_delete_own_account(request):
            if not auth_is_not_delegated(request):
                return False

            return request.settings.allow_delete_own_account

        usercp.add_section(
            link="misago:usercp-delete-account",
            name=pgettext_lazy("user options page", "Delete account"),
            component="delete-account",
            icon="cancel",
            visible_if=can_delete_own_account,
        )

    def register_default_users_list_pages(self):
        users_list.add_section(
            link="misago:users-active-posters",
            component="active-posters",
            name=pgettext_lazy("users lists page", "Top posters"),
        )

    def register_default_user_profile_pages(self):
        def can_see_names_history(request, profile):
            if request.user.is_authenticated:
                is_account_owner = profile.pk == request.user.pk
                has_permission = request.user_acl["can_see_users_name_history"]
                return is_account_owner or has_permission
            return False

        def can_see_ban_details(request, profile):
            if request.user.is_authenticated:
                if request.user_acl["can_see_ban_details"]:
                    from .bans import get_user_ban

                    return bool(get_user_ban(profile, request.cache_versions))
                return False
            return False

        user_profile.add_section(
            link="misago:user-posts",
            name=pgettext_lazy("user profile page", "Posts"),
            icon="message",
            component="posts",
        )
        user_profile.add_section(
            link="misago:user-threads",
            name=pgettext_lazy("user profile page", "Threads"),
            icon="forum",
            component="threads",
        )
        user_profile.add_section(
            link="misago:user-followers",
            name=pgettext_lazy("user profile page", "Followers"),
            icon="favorite",
            component="followers",
        )
        user_profile.add_section(
            link="misago:user-follows",
            name=pgettext_lazy("user profile page", "Follows"),
            icon="favorite_border",
            component="follows",
        )
        user_profile.add_section(
            link="misago:user-details",
            name=pgettext_lazy("user profile page", "Details"),
            icon="person_outline",
            component="details",
        )
        user_profile.add_section(
            link="misago:username-history",
            name=pgettext_lazy("user profile page", "Username history"),
            icon="card_membership",
            component="username-history",
            visible_if=can_see_names_history,
        )
        user_profile.add_section(
            link="misago:user-ban",
            name=pgettext_lazy("user profile page", "Ban details"),
            icon="remove_circle_outline",
            component="ban-details",
            visible_if=can_see_ban_details,
        )
