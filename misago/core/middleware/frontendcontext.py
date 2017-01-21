from django.utils.deprecation import MiddlewareMixin


class FrontendContextMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.include_frontend_context = True
        request.frontend_context = {}
