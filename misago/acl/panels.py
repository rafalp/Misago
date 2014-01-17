from debug_toolbar.panels import Panel
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _

class MisagoACLDebugPanel(Panel):
    name = 'MisagoACL'
    has_content = True

    def nav_title(self):
        return _('Misago ACL')

    def title(self):
        return _('Misago User ACL')

    def url(self):
        return ''

    def process_request(self, request):
        self.request = request

    def content(self):
        if self.request.heartbeat:
            self.has_content = False
        else:
            context = self.context.copy()
            try:
                context['acl'] = self.request.acl
            except AttributeError:
                context['acl'] = {}
            return render_to_string('debug_toolbar/panels/acl.html', context)
