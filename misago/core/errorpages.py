from django.http import JsonResponse
from django.shortcuts import render
from django.utils.translation import ugettext as _
from social_core import exceptions as social_exceptions

from misago.admin.views.errorpages import admin_csrf_failure, admin_error_page
from misago.core.exceptions import SocialAuthFailed, SocialAuthBanned
from misago.users.social.utils import get_social_auth_backend_name

from .utils import get_exception_message, is_request_to_misago


def _ajax_error(code, exception=None, default_message=None):
    return JsonResponse({
        'detail': get_exception_message(exception, default_message),
    }, status=code)


@admin_error_page
def _error_page(request, code, exception=None, default_message=None):
    return render(
        request, 'misago/errorpages/%s.html' % code, {
            'message': get_exception_message(exception, default_message),
        }, status=code
    )


def banned(request, exception):
    ban = exception.ban

    request.frontend_context['store'].update({
        'error': {
            'ban': ban.get_serialized_message(),
        },
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


def social_auth_failed(request, exception):
    backend_name = None
    ban = None
    help_text = None
    message = None

    try:
        backend_name = exception.backend_name
    except AttributeError:
        pass
    try:
        exception_backend = exception.backend
        backend_name = get_social_auth_backend_name(exception_backend.name)
    except AttributeError:
        pass

    if isinstance(exception, social_exceptions.NotAllowedToDisconnect):
        message = _(
            "A problem was encountered when disconnecting your account from the remote site."
        )
        help_text = _(
            "You are not allowed to disconnect your account from the other site, "
            "because currently it's the only way to sign in to your account."
        )
    elif backend_name:
        message = _("A problem was encountered when signing you in using %(backend)s.") % {
            'backend': backend_name
        }

        if isinstance(exception, social_exceptions.AuthCanceled):
            help_text = _("The sign in process has been canceled by user.")
        if isinstance(exception, social_exceptions.AuthUnreachableProvider):
            help_text = _("The other service could not be reached.")
        if isinstance(exception, SocialAuthFailed):
            help_text = exception.message
        if isinstance(exception, SocialAuthBanned):
            ban = exception.ban
    else:
        message = _("Unexpected problem has been encountered during sign in process.")

    return render(request, 'misago/errorpages/social.html', {
        'backend_name': backend_name,
        'ban': ban,
        'message': message,
        'help_text': help_text,
    }, status=403)


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
