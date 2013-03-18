from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from misago.admin import ADMIN_PATH
from misago.messages import Message
from misago.apps.errors import error403, error404
from misago.apps.signin.views import signin

class FirewallForum(object):
    admin = False
    prefix = ''

    def behind_firewall(self, path):
        """
        Firewall test, it checks if requested path is behind firewall
        """
        return path[:len(self.prefix)] == self.prefix

    def process_view(self, request, callback, callback_args, callback_kwargs):
        return None


class FirewallAdmin(FirewallForum):
    admin = True
    prefix = '/' + ADMIN_PATH

    def process_view(self, request, callback, callback_args, callback_kwargs):
        # Block all crawlers with 403
        if request.user.is_crawler():
            request.theme.reset_theme()
            return error403(request)
        else:
            # If we are not authenticated or not admin, force us to sign in right way
            if not request.user.is_authenticated():
                return signin(request)
            elif not request.user.is_god() and not request.acl.admin.is_admin():
                request.messages.set_message(Message(_("Your account does not have admin privileges")), 'error', 'security')
                return signin(request)
            return None
