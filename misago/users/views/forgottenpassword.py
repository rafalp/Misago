from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils.translation import gettext as _

from ...core.exceptions import Banned
from ..bans import get_user_ban
from ..decorators import deny_banned_ips
from ..tokens import is_password_change_token_valid


def reset_view(f):
    @deny_banned_ips
    def decorator(*args, **kwargs):
        return f(*args, **kwargs)

    return decorator


@reset_view
def request_reset(request):
    request.frontend_context.update(
        {"SEND_PASSWORD_RESET_API": reverse("misago:api:send-password-form")}
    )
    return render(request, "misago/forgottenpassword/request.html")


class ResetError(Exception):
    pass


@reset_view
def reset_password_form(request, pk, token):
    requesting_user = get_object_or_404(get_user_model(), pk=pk)

    try:
        if request.user.is_authenticated and request.user.id != requesting_user.id:
            message = _(
                "%(user)s, your link has expired. "
                "Please request new link and try again."
            )
            raise ResetError(message % {"user": requesting_user.username})

        if not is_password_change_token_valid(requesting_user, token):
            message = _(
                "%(user)s, your link is invalid. Please try again or request new link."
            )
            raise ResetError(message % {"user": requesting_user.username})

        ban = get_user_ban(requesting_user, request.cache_versions)
        if ban:
            raise Banned(ban)
    except ResetError as e:
        return render(
            request,
            "misago/forgottenpassword/error.html",
            {"message": e.args[0]},
            status=400,
        )

    api_url = reverse(
        "misago:api:change-forgotten-password", kwargs={"pk": pk, "token": token}
    )

    request.frontend_context["CHANGE_PASSWORD_API"] = api_url
    return render(request, "misago/forgottenpassword/form.html")
