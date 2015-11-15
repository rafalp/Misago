from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, render
from django.utils.translation import ugettext as _

from misago.conf import settings
from misago.core.mail import mail_user
from misago.core.exceptions import Banned

from misago.users.bans import get_user_ban
from misago.users.decorators import deny_authenticated, deny_banned_ips
from misago.users.models import ACTIVATION_REQUIRED_NONE
from misago.users.tokens import is_activation_token_valid


def activation_view(f):
    @deny_authenticated
    @deny_banned_ips
    def decorator(*args, **kwargs):
        return f(*args, **kwargs)
    return decorator


@activation_view
def request_activation(request):
    request.frontend_context.update({
        'SEND_ACTIVATION_API_URL': reverse('misago:api:send_activation')
    })
    return render(request, 'misago/activation/request.html')


class ActivationStopped(Exception):
    pass


class ActivationError(Exception):
    pass


@activation_view
def activate_by_token(request, user_id, token):
    User = get_user_model()
    inactive_user = get_object_or_404(User.objects, pk=user_id)

    try:
        if not inactive_user.requires_activation:
            message = _("%(user)s, your account is already active.")
            message = message % {'user': inactive_user.username}
            raise ActivationStopped(message)
        if inactive_user.requires_activation_by_admin:
            message = _("%(user)s, your account can be activated "
                        "only by one of the administrators.")
            message = message % {'user': inactive_user.username}
            raise ActivationStopped(message)

        if not is_activation_token_valid(inactive_user, token):
            message = _("%(user)s, your activation link is invalid. "
                        "Try again or request new activation link.")
            message = message % {'user': inactive_user.username}
            raise ActivationError(message)

        ban = get_user_ban(inactive_user)
        if ban:
            raise Banned(ban)
    except ActivationStopped as e:
        return render(request, 'misago/activation/stopped.html', {
                'message': e.args[0],
            })
    except ActivationError as e:
        return render(request, 'misago/activation/error.html', {
                'message': e.args[0],
            }, status=400)

    inactive_user.requires_activation = ACTIVATION_REQUIRED_NONE
    inactive_user.save(update_fields=['requires_activation'])

    message = _("%(user)s, your account has been activated!")

    return render(request, 'misago/activation/done.html', {
            'message': message % {'user': inactive_user.username},
        })
