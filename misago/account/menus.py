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
account_settings_menu.add_item(
    key="username",
    url_name="misago:account-username",
    label=pgettext_lazy("account settings page", "Username"),
    icon="card_membership",
)


def auth_is_not_delegated(request: HttpRequest) -> bool:
    return not request.settings.enable_oauth2_client


def can_delete_own_account(request: HttpRequest) -> bool:
    if not auth_is_not_delegated(request):
        return False

    return request.settings.allow_delete_own_account


account_settings_menu.add_item(
    key="delete",
    url_name="misago:account-delete",
    label=pgettext_lazy("account settings page", "Delete account"),
    icon="cancel",
    visible=can_delete_own_account,
)
