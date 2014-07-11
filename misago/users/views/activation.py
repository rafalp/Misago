from django.contrib import messages
from django.contrib.auth import get_user_model
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import ugettext as _

from misago.conf import settings
from misago.users.decorators import deny_authenticated, deny_banned_ips
from misago.users.models import (ACTIVATION_REQUIRED_NONE,
                                 ACTIVATION_REQUIRED_USER,
                                 ACTIVATION_REQUIRED_ADMIN)
from misago.users.tokens import (make_activation_token,
                                 is_activation_token_valid)


class ActivationStopped(Exception):
    pass


class ActivationError(Exception):
    pass


@deny_authenticated
@deny_banned_ips
def activate_by_token(request, user_id, token):
    User = get_user_model()
    inactive_user = get_object_or_404(User.objects, pk=user_id)

    try:
        if not inactive_user.requires_activation:
            message = _("%(username)s, your account is already active.")
            message = message % {'username': inactive_user.username}
            raise ActivationStopped(message)
        if inactive_user.requires_activation == ACTIVATION_REQUIRED_ADMIN:
            message = _("%(username)s, your account can be activated "
                        "only by one ofthe  administrators.")
            message = message % {'username': inactive_user.username}
            raise ActivationStopped(message)
        if not is_activation_token_valid(inactive_user, token):
            message = _("%(username)s, your activation link is invalid. "
                        "Try again or request new activation message.")
            message = message % {'username': inactive_user.username}
            raise ActivationError(message)
    except ActivationStopped as e:
        messages.info(request, e.args[0])
        return redirect('misago:index')
    except ActivationError as e:
        messages.error(request, e.args[0])
        return redirect('misago:index')

    inactive_user.requires_activation = ACTIVATION_REQUIRED_NONE
    inactive_user.save(update_fields=['requires_activation'])

    message = _("%(username)s, your account has been activated!")
    message = message % {'username': inactive_user.username}
    messages.success(request, message)

    return redirect(settings.LOGIN_URL)
