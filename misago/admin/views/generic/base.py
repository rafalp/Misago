from django.views import View

from misago.admin.views import render


class AdminView(View):
    def final_template(self):
        return '%s/%s' % (self.templates_dir, self.template)

    def current_link(self, request):
        matched_url = request.resolver_match.url_name
        return '%s:%s' % (request.resolver_match.namespace, matched_url)

    def process_context(self, request, context):
        """simple hook for extending and manipulating template context."""
        return context

    def render(self, request, context=None, template=None):
        context = context or {}

        context['root_link'] = self.root_link
        context['current_link'] = self.current_link(request)

        context = self.process_context(request, context)

        template = template or self.final_template()
        return render(request, template, context)
