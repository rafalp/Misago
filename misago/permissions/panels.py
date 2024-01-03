from debug_toolbar.panels import Panel
from django.utils.translation import pgettext_lazy


class MisagoUserPermissionsPanel(Panel):
    """Panel that displays current user's permission"""

    title = pgettext_lazy("debug toolbar", "Misago User Permissions")
    nav_title = pgettext_lazy("debug toolbar", "Misago Permissions")
    template = "misago/permissions_panel.html"

    @property
    def nav_subtitle(self):
        misago_user = self.get_stats().get("misago_user")

        if misago_user and misago_user.is_authenticated:
            return misago_user.username
        return pgettext_lazy("debug toolbar", "Anonymous user")

    def generate_stats(self, request, response):
        try:
            misago_user = request.user
        except AttributeError:
            misago_user = None

        try:
            misago_permissions = request.user_permissions
        except AttributeError:
            misago_permissions = None

        self.record_stats(
            {
                "misago_user": misago_user,
                "misago_permissions": misago_permissions,
            }
        )
