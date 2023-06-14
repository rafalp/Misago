from debug_toolbar.panels import Panel
from django.utils.translation import pgettext_lazy


class MisagoACLPanel(Panel):
    """panel that displays current user's ACL"""

    title = pgettext_lazy("debug toolbar", "Misago User ACL")
    template = "misago/acl_debug.html"

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
            misago_acl = request.user_acl
        except AttributeError:
            misago_acl = {}

        self.record_stats({"misago_user": misago_user, "misago_acl": misago_acl})
