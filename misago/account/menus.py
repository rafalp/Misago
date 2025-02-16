from django.conf import settings
from django.http import HttpRequest
from django.utils.translation import pgettext_lazy

from ..menus.menu import Menu


account_settings_menu = Menu()

account_settings_menu.add_item(
    key="preferences",
    url_name="misago:account-preferences",
    label=pgettext_lazy("account settings page", "Preferences"),
    icon="tune",
)


def show_profile_details(request: HttpRequest) -> bool:
    return bool(settings.MISAGO_PROFILE_FIELDS)


account_settings_menu.add_item(
    key="details",
    url_name="misago:account-details",
    label=pgettext_lazy("account settings page", "Profile details"),
    icon="person_outline",
    visible=show_profile_details,
)


account_settings_menu.add_item(
    key="attachments",
    url_name="misago:account-attachments",
    label=pgettext_lazy("account settings page", "Attachments"),
    icon="file_download",
)


def auth_is_not_delegated(request: HttpRequest) -> bool:
    return not request.settings.enable_oauth2_client


account_settings_menu.add_item(
    key="username",
    url_name="misago:account-username",
    label=pgettext_lazy("account settings page", "Username"),
    icon="card_membership",
    visible=auth_is_not_delegated,
)


account_settings_menu.add_item(
    key="password",
    url_name="misago:account-password",
    label=pgettext_lazy("account settings page", "Password"),
    icon="vpn_key",
    visible=auth_is_not_delegated,
)


account_settings_menu.add_item(
    key="email",
    url_name="misago:account-email",
    label=pgettext_lazy("account settings page", "Email address"),
    icon="mail_outline",
    visible=auth_is_not_delegated,
)


def show_download_data(request: HttpRequest) -> bool:
    return request.settings.allow_data_downloads


account_settings_menu.add_item(
    key="download-data",
    url_name="misago:account-download-data",
    label=pgettext_lazy("account settings page", "Download data"),
    icon="save_alt",
    visible=show_download_data,
)


def show_delete_own_account(request: HttpRequest) -> bool:
    if not auth_is_not_delegated(request):
        return False

    return request.settings.allow_delete_own_account


account_settings_menu.add_item(
    key="delete",
    url_name="misago:account-delete",
    label=pgettext_lazy("account settings page", "Delete account"),
    icon="cancel",
    visible=show_delete_own_account,
)
