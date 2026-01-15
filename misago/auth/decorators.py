from functools import wraps
from typing import Callable

from django.core.exceptions import PermissionDenied
from django.utils.functional import Promise
from django.utils.translation import pgettext

from .views import is_misago_login_page_disabled, login


def login_required(f_or_message: Callable | Promise | str):
    if isinstance(f_or_message, (Promise, str)):

        def _outer_login_required_decorator(f):
            return _create_login_required_decorator(f, f_or_message)

        return _outer_login_required_decorator

    return _create_login_required_decorator(f_or_message)


def _create_login_required_decorator(f: Callable, message: Promise | str | None = None):
    @wraps(f)
    def login_required_decorator(request, *args, **kwargs):
        login_message = message or pgettext(
            "login required decorator", "Sign in to continue"
        )

        if not request.user.is_authenticated:
            if request.is_htmx or is_misago_login_page_disabled():
                raise PermissionDenied(login_message)

            return login(
                request,
                message=login_message,
                next=request.get_full_path(),
                status=401,
            )

        return f(request, *args, **kwargs)

    return login_required_decorator
