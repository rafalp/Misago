from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin


class FrontendContextMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.include_frontend_context = True
        request.frontend_context = {
            'auth': {},
            'conf': {},
            'store': {},

            'api': '{}api/'.format(reverse('misago:index')),
            'url': {},
        }
