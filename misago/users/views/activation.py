from django.contrib import messages
from django.contrib.auth import get_user_model
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import ugettext as _

from misago.conf import settings
from misago.core.mail import mail_user

from misago.users.bans import get_user_ban
from misago.users.decorators import deny_authenticated, deny_banned_ips
from misago.users.forms.auth import ResendActivationForm
from misago.users.models import ACTIVATION_REQUIRED_NONE
from misago.users.tokens import (make_activation_token,
                                 is_activation_token_valid)


def activation_view(f):
    @deny_authenticated
    @deny_banned_ips
    def decorator(*args, **kwargs):
        return f(*args, **kwargs)
    return decorator


@activation_view
def request_activation(request):
    form = ResendActivationForm()

    if request.method == 'POST':
        form = ResendActivationForm(request.POST)
        if form.is_valid():
            requesting_user = form.user_cache
            request.session['activation_sent_to'] = requesting_user.pk

            mail_subject = _("Account activation on %(forum_title)s forums")
            mail_subject = mail_subject % {'forum_title': settings.forum_name}

            activation_token = make_activation_token(requesting_user)

            mail_user(
                request, requesting_user, mail_subject,
                'misago/emails/activation/by_user',
                {'activation_token': activation_token})

            return redirect('misago:activation_sent')

    return render(request, 'misago/activation/request.html',
                  {'form': form})


@activation_view
def activation_sent(request):
    requesting_user_pk = request.session.get('activation_sent_to')
    if not requesting_user_pk:
        raise Http404()

    User = get_user_model()
    requesting_user = get_object_or_404(User.objects, pk=requesting_user_pk)

    return render(request, 'misago/activation/sent.html',
                  {'requesting_user': requesting_user})


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
        if get_user_ban(inactive_user):
            message = _("%(user)s, your account is banned "
                        "and can't be activated.")
            message = message % {'user': inactive_user.username}
            raise ActivationError(message)
        if not is_activation_token_valid(inactive_user, token):
            message = _("%(user)s, your activation link is invalid. "
                        "Try again or request new activation message.")
            message = message % {'user': inactive_user.username}
            raise ActivationError(message)
    except ActivationStopped as e:
        messages.info(request, e.args[0])
        return redirect('misago:index')
    except ActivationError as e:
        messages.error(request, e.args[0])
        return redirect('misago:request_activation')

    inactive_user.requires_activation = ACTIVATION_REQUIRED_NONE
    inactive_user.save(update_fields=['requires_activation'])

    message = _("%(user)s, your account has been activated!")
    message = message % {'user': inactive_user.username}
    messages.success(request, message)

    return redirect(settings.LOGIN_URL)
