from django.http import JsonResponse
from django.shortcuts import render
from django.utils.translation import ugettext as _

from misago.core.utils import is_request_to_misago
from misago.admin.views.errorpages import admin_error_page, admin_csrf_failure


def _ajax_error(code=406, message=None):
    response_dict = {'is_error': True}
    if message:
        response_dict['message'] = unicode(message)
    return JsonResponse(response_dict, status=code)


@admin_error_page
def _error_page(request, code, message=None):
    response = render(request,
                      'misago/errorpages/%s.html' % code,
                      {'message': message})
    response.status_code = code
    return response


def permission_denied(request, message=None):
    if request.is_ajax():
        return _ajax_error(403, message)
    else:
        return _error_page(request, 403, message)


def page_not_found(request):
    if request.is_ajax():
        return _ajax_error(404, _("Invalid API link."))
    else:
        return _error_page(request, 404)


@admin_csrf_failure
def csrf_failure(request, reason=""):
    if request.is_ajax():
        return _ajax_error(403, _("Request authentication is invalid."))
    else:
        response = render(request, 'misago/errorpages/csrf_failure.html')
        response.status_code = 403
        return response


def not_allowed(request):
    response = render(request, 'misago/errorpages/405.html')
    response.status_code = 405
    return response


# Decorators for custom error page handlers
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
