from .exceptionhandler import (
    handle_misago_exception,
    handle_misago_htmx_exception,
    is_misago_exception,
)
from .utils import is_request_to_misago


class ExceptionHandlerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_exception(self, request, exception):
        if not is_request_to_misago(request):
            return

        if request.is_htmx and is_misago_exception(exception, True):
            return handle_misago_htmx_exception(exception)

        if is_misago_exception(exception):
            return handle_misago_exception(request, exception)


class FrontendContextMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.include_frontend_context = True
        request.frontend_context = {}
        return self.get_response(request)
