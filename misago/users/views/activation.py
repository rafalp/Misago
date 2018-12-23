from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils.translation import gettext as _

from ...core.exceptions import Banned
from ..bans import get_user_ban
from ..decorators import deny_authenticated, deny_banned_ips
from ..tokens import is_activation_token_valid

User = get_user_model()


def activation_view(f):
    @deny_authenticated
    @deny_banned_ips
    def decorator(*args, **kwargs):
        return f(*args, **kwargs)

    return decorator


@activation_view
def request_activation(request):
    request.frontend_context.update(
        {"SEND_ACTIVATION_API": reverse("misago:api:send-activation")}
    )
    return render(request, "misago/activation/request.html")


class ActivationStopped(Exception):
    pass


class ActivationError(Exception):
    pass


@activation_view
def activate_by_token(request, pk, token):
    inactive_user = get_object_or_404(User, pk=pk, is_active=True)

    try:
        if not inactive_user.requires_activation:
            message = _("%(user)s, your account is already active.")
            raise ActivationStopped(message % {"user": inactive_user.username})

        if not is_activation_token_valid(inactive_user, token):
            message = _(
                "%(user)s, your activation link is invalid. "
                "Try again or request new activation link."
            )
            raise ActivationError(message % {"user": inactive_user.username})

        ban = get_user_ban(inactive_user, request.cache_versions)
        if ban:
            raise Banned(ban)
    except ActivationStopped as e:
        return render(request, "misago/activation/stopped.html", {"message": e.args[0]})
    except ActivationError as e:
        return render(
            request, "misago/activation/error.html", {"message": e.args[0]}, status=400
        )

    inactive_user.requires_activation = User.ACTIVATION_NONE
    inactive_user.save(update_fields=["requires_activation"])

    message = _("%(user)s, your account has been activated!")

    return render(
        request,
        "misago/activation/done.html",
        {"message": message % {"user": inactive_user.username}},
    )
