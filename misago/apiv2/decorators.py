from functools import wraps

from django.core.exceptions import PermissionDenied
from django.utils.translation import gettext as _


def require_auth(f):
    @wraps(f)
    def auth_only_view(request, *args, **kwargs):
        if request.user.is_anonymous:
            if request.method in ("GET", "HEAD", "OPTIONS"):
                raise PermissionDenied(_("You have to sign in to access this page."))
            raise PermissionDenied(_("You have to sign in to perform this action."))

        return f(request, *args, **kwargs)

    return auth_only_view
