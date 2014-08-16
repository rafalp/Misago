from debug_toolbar.panels import Panel
from django.utils.translation import ugettext_lazy as _


class MisagoACLPanel(Panel):
    """
    Panel that displays current user's ACL
    """
    title = _('Misago User ACL')
    template = 'misago/acl_debug.html'

    @property
    def nav_subtitle(self):
        misago_user = self.get_stats().get('misago_user')

        if misago_user.is_authenticated():
            return misago_user.username
        else:
            return _("Anonymous user")

    def process_response(self, request, response):
        try:
            misago_acl = request.user.acl
        except AttributeError:
            misago_acl = {}

        self.record_stats({
            'misago_user': request.user,
            'misago_acl': misago_acl,
        })
