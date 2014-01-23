from django.shortcuts import render


def _error_page(request, code, message=None):
    response = render(request,
                      'misago/front/%s.html' % code,
                      {'message': message})
    response.status_code = code
    return response


def permission_denied(request, message=None):
    return _error_page(request, 403, message)


def page_not_found(request):
    return _error_page(request, 404)


"""
Decorators for custom error page handlers
"""
from misago.views.utils import is_request_to_misago


def shared_403_exception_handler(f):
    def page_decorator(request, *args, **kwargs):
        if is_request_to_misago(request):
            return permission_denied(request)
        else:
            return f(request, *args, **kwargs)
    return page_decorator


def shared_404_exception_handler(f):
    def page_decorator(request, *args, **kwargs):
        if is_request_to_misago(request):
            return page_not_found(request)
        else:
            return f(request, *args, **kwargs)
    return page_decorator
