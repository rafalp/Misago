from django.http import JsonResponse
from django.shortcuts import render
from django.utils.translation import ugettext as _

from misago.admin.views.errorpages import admin_csrf_failure, admin_error_page

from .utils import get_exception_message, is_request_to_misago


def _ajax_error(code, exception=None, default_message=None):
    return JsonResponse({
        'detail': get_exception_message(exception, default_message),
    }, status=code)


@admin_error_page
def _error_page(request, code, exception=None, default_message=None):
    request.frontend_context.update({
        'CURRENT_LINK': 'misago:error-%s' % code,
    })

    return render(
        request, 'misago/errorpages/%s.html' % code, {
            'message': get_exception_message(exception, default_message),
        }, status=code
    )


def banned(request, exception):
    ban = exception.ban

    request.frontend_context.update({
        'MESSAGE': ban.get_serialized_message(),
        'CURRENT_LINK': 'misago:error-banned',
    })

    return render(
        request, 'misago/errorpages/banned.html', {
            'ban': ban,
        }, status=403
    )


def permission_denied(request, exception):
    if request.is_ajax():
        return _ajax_error(403, exception, _("Permission denied."))
    else:
        return _error_page(request, 403, exception)


def page_not_found(request, exception):
    if request.is_ajax():
        return _ajax_error(404, exception, "Not found.")
    else:
        return _error_page(request, 404, exception)


@admin_csrf_failure
def csrf_failure(request, reason=""):
    if request.is_ajax():
        return _ajax_error(403, _("Request authentication is invalid."))
    else:
        response = render(request, 'misago/errorpages/csrf_failure.html')
        response.status_code = 403
        return response


def not_allowed(request):
    return _error_page(request, 405)


# Decorators for custom error page handlers
def shared_403_exception_handler(f):
    def page_decorator(request, *args, **kwargs):
        if is_request_to_misago(request):
            return permission_denied(request, *args, **kwargs)
        else:
            return f(request, *args, **kwargs)

    return page_decorator


def shared_404_exception_handler(f):
    def page_decorator(request, *args, **kwargs):
        if is_request_to_misago(request):
            return page_not_found(request, *args, **kwargs)
        else:
            return f(request, *args, **kwargs)

    return page_decorator
