from django.conf import settings
from misago.admin import ADMIN_PATH
from misago.views import error403, error404
from misago.security.views import signin

class FirewallForum(object):
    """
    Firewall Abstraction
    """
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
            else:
                return None