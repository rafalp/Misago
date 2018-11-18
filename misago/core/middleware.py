from django.utils.deprecation import MiddlewareMixin

from misago.core import exceptionhandler, threadstore
from misago.core.utils import is_request_to_misago


class ExceptionHandlerMiddleware(MiddlewareMixin):
    def process_exception(self, request, exception):
        request_is_to_misago = is_request_to_misago(request)
        misago_can_handle_exception = exceptionhandler.is_misago_exception(exception)

        if request_is_to_misago and misago_can_handle_exception:
            return exceptionhandler.handle_misago_exception(request, exception)
        else:
            return None


class FrontendContextMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.include_frontend_context = True
        request.frontend_context = {}


class ThreadStoreMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        threadstore.clear()
        return response
