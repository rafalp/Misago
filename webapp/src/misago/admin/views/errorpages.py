from django.shortcuts import redirect, render as dj_render

from . import get_protected_namespace, protected_admin_view, render
from ...core.utils import get_exception_message
from ..auth import is_admin_authorized, update_admin_authorization

# Magic error page used by admin
@protected_admin_view
def _error_page(request, code, exception=None, default_message=None):
    if not is_admin_authorized(request):
        return redirect("misago:admin:index")

    template_pattern = "misago/admin/errorpages/%s.html" % code

    response = render(
        request,
        template_pattern,
        {"message": get_exception_message(exception, default_message)},
        error_page=True,
    )
    response.status_code = code
    return response


def admin_error_page(f):
    def decorator(request, *args, **kwargs):
        if get_protected_namespace(request):
            update_admin_authorization(request)
            return _error_page(request, *args, **kwargs)
        return f(request, *args, **kwargs)

    return decorator


# Magic CSRF fail page for Admin
def _csrf_failure(request, reason=""):
    if is_admin_authorized(request):
        update_admin_authorization(request)
        response = render(
            request,
            "misago/admin/errorpages/csrf_failure_authenticated.html",
            error_page=True,
        )
    else:
        response = dj_render(request, "misago/admin/errorpages/csrf_failure.html")

    response.status_code = 403
    return response


def admin_csrf_failure(f):
    def decorator(request, *args, **kwargs):
        if get_protected_namespace(request):
            return _csrf_failure(request, *args, **kwargs)
        return f(request, *args, **kwargs)

    return decorator
