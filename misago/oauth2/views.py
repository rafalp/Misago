from functools import wraps
from logging import getLogger

from django.contrib.auth import get_user_model, login
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.cache import never_cache

from ..core.exceptions import Banned
from ..users.bans import get_user_ban
from ..users.decorators import deny_banned_ips
from ..users.registration import send_welcome_email
from .client import (
    create_login_url,
    get_access_token,
    get_code_grant,
    get_user_data,
)
from .exceptions import (
    OAuth2Error,
    OAuth2UserAccountDeactivatedError,
    OAuth2UserDataValidationError,
)
from .user import get_user_from_data

logger = getLogger("misago.oauth2")

User = get_user_model()


def oauth2_view(f):
    f = deny_banned_ips(f)

    @wraps(f)
    @never_cache
    def wrapped_oauth2_view(request):
        if not request.settings.enable_oauth2_client:
            raise Http404()

        return f(request)

    return wrapped_oauth2_view


@oauth2_view
def oauth2_login(request):
    redirect_to = create_login_url(request)
    return redirect(redirect_to)


@oauth2_view
def oauth2_complete(request):
    try:
        code_grant = get_code_grant(request)
        token = get_access_token(request, code_grant)
        user_data, response_json = get_user_data(request, token)
        user, created = get_user_from_data(request, user_data, response_json)

        if not user.is_active:
            raise OAuth2UserAccountDeactivatedError()

        if not user.is_misago_admin:
            if user_ban := get_user_ban(user, request.cache_versions):
                raise Banned(user_ban)
    except OAuth2UserDataValidationError as error:
        logger.exception(
            "OAuth2 Profile Error",
            extra={
                f"error[{error_index}]": str(error_msg)
                for error_index, error_msg in enumerate(error.error_list)
            },
        )
        return render(
            request,
            "misago/errorpages/oauth2_profile.html",
            {
                "error": error,
                "error_list": error.error_list,
            },
            status=400,
        )
    except OAuth2Error as error:
        logger.exception("OAuth2 Error")
        return render(
            request,
            "misago/errorpages/oauth2.html",
            {"error": error},
            status=400,
        )

    if created and request.settings.oauth2_send_welcome_email:
        send_welcome_email(request, user)

    if not user.requires_activation:
        login(request, user)

    return redirect(reverse("misago:index"))
