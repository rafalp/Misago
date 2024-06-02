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


def auth_is_not_delegated(request: HttpRequest) -> bool:
    return not request.settings.enable_oauth2_client


account_settings_menu.add_item(
    key="username",
    url_name="misago:account-username",
    label=pgettext_lazy("account settings page", "Username"),
    icon="card_membership",
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
