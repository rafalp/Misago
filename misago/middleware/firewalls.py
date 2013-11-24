from django.conf import settings
from misago.firewalls import *
from misago.template.theme import activate_theme

class FirewallMiddleware(object):
    firewall_admin = FirewallAdmin()
    firewall_forum = FirewallForum()

    def process_request(self, request):
        if settings.ADMIN_PATH and self.firewall_admin.behind_firewall(request.path_info):
            request.firewall = self.firewall_admin
            activate_theme('admin')
        else:
            request.firewall = self.firewall_forum

    def process_view(self, request, callback, callback_args, callback_kwargs):
        return request.firewall.process_view(request, callback, callback_args, callback_kwargs)
