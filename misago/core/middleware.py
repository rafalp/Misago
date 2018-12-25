from django.utils.deprecation import MiddlewareMixin

from . import exceptionhandler
from .utils import is_request_to_misago


class ExceptionHandlerMiddleware(MiddlewareMixin):
    def process_exception(self, request, exception):
        request_is_to_misago = is_request_to_misago(request)
        misago_can_handle_exception = exceptionhandler.is_misago_exception(exception)

        if request_is_to_misago and misago_can_handle_exception:
            return exceptionhandler.handle_misago_exception(request, exception)


class FrontendContextMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.include_frontend_context = True
        request.frontend_context = {}
