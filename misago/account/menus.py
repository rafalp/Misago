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
