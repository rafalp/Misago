from django.views import View

from .. import render


class AdminView(View):
    def get_template_name(self, request):
        return "%s/%s" % (self.templates_dir, self.template_name)

    def current_link(self, request):
        matched_url = request.resolver_match.url_name
        return "%s:%s" % (request.resolver_match.namespace, matched_url)

    def process_context(self, request, context):
        """simple hook for extending and manipulating template context."""
        return context

    def render(self, request, context=None, template_name=None):
        context = context or {}

        context["root_link"] = self.root_link
        context["current_link"] = self.current_link(request)

        context = self.process_context(request, context)

        template_name = template_name or self.get_template_name(request)
        return render(request, template_name, context)
