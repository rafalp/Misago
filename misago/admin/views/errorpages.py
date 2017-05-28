from django.shortcuts import redirect

from misago.admin.auth import is_admin_session, update_admin_session
from misago.core.utils import get_exception_message

from . import get_protected_namespace, protected_admin_view, render


# Magic error page used by admin
@protected_admin_view
def _error_page(request, code, exception=None, default_message=None):
    if is_admin_session(request):
        template_pattern = 'misago/admin/errorpages/%s.html' % code

        response = render(request, template_pattern, {
            'message': get_exception_message(exception, default_message),
        }, error_page=True)
        response.status_code = code
        return response
    else:
        return redirect('misago:admin:index')


def admin_error_page(f):
    def decorator(request, *args, **kwargs):
        if get_protected_namespace(request):
            update_admin_session(request)
            return _error_page(request, *args, **kwargs)
        else:
            return f(request, *args, **kwargs)

    return decorator


# Magic CSRF fail page for Admin
def _csrf_failure(request, reason=""):
    if is_admin_session(request):
        update_admin_session(request)
        response = render(
            request,
            'misago/admin/errorpages/csrf_failure_authenticated.html',
            error_page=True,
        )
    else:
        response = render(request, 'misago/admin/errorpages/csrf_failure.html')

    response.status_code = 403
    return response


def admin_csrf_failure(f):
    def decorator(request, *args, **kwargs):
        if get_protected_namespace(request):
            return _csrf_failure(request, *args, **kwargs)
        else:
            return f(request, *args, **kwargs)

    return decorator
