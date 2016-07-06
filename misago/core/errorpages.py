from django.http import JsonResponse
from django.shortcuts import render
from django.utils.translation import ugettext as _

from misago.admin.views.errorpages import admin_csrf_failure, admin_error_page
from misago.core.utils import is_request_to_misago


def _ajax_error(code=406, message=None):
    return JsonResponse({'detail': message}, status=code)


@admin_error_page
def _error_page(request, code, message=None):
    return render(request, 'misago/errorpages/%s.html' % code, {
            'message': message
        }, status=code)


def banned(request, ban):
    request.frontend_context['BAN_MESSAGE'] = ban.get_serialized_message()

    return render(request, 'misago/errorpages/banned.html', {
            'ban': ban
        }, status=403)


def permission_denied(request, message=None):
    if request.is_ajax():
        return _ajax_error(403, message or _("Permission denied."))
    else:
        return _error_page(request, 403, message)


def page_not_found(request):
    if request.is_ajax():
        return _ajax_error(404, "Not found.")
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
