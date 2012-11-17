from django.conf import settings
from misago.security import get_random_string
from misago.security.csrf import CSRFProtection
from misago.security.firewalls import *
from misago.security.models import JamCache
from misago.themes.theme import Theme

class FirewallMiddleware(object):
    firewall_admin = FirewallAdmin()
    firewall_forum = FirewallForum()
    def process_request(self, request):
        # Admin firewall test
        if settings.ADMIN_PATH and self.firewall_admin.behind_firewall(request.path_info):
            request.firewall = self.firewall_admin
            request.theme.set_theme('admin')
        else:
            request.firewall = self.firewall_forum

    def process_view(self, request, callback, callback_args, callback_kwargs):
        return request.firewall.process_view(request, callback, callback_args, callback_kwargs)

class JamMiddleware(object):
    def process_request(self, request):
        if request.user.is_crawler():
            return None
        try:
            request.jam = request.session['jam']
        except KeyError:
            request.jam = JamCache()
            request.session['jam'] = request.jam
        if not request.firewall.admin:
            request.jam.check_for_updates(request)

class CSRFMiddleware(object):
    def process_request(self, request):
        if request.user.is_crawler():
            return None
        if 'csrf_token' in request.session:
            csrf_token = request.session['csrf_token']
        else:
            csrf_token = get_random_string(16);
            request.session['csrf_token'] = csrf_token
        request.csrf = CSRFProtection(csrf_token)