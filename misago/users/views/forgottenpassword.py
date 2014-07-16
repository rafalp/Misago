from faker import Factory
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import ugettext as _

from misago.conf import settings
from misago.core.mail import mail_user

from misago.users.bans import get_user_ban
from misago.users.decorators import deny_authenticated, deny_banned_ips
from misago.users.forms.auth import ResetPasswordForm
from misago.users.models import ACTIVATION_REQUIRED_NONE
from misago.users.tokens import (make_password_reset_token,
                                 is_password_reset_token_valid)


def reset_view(f):
    @deny_authenticated
    @deny_banned_ips
    def decorator(*args, **kwargs):
        return f(*args, **kwargs)
    return decorator


@reset_view
def request_reset(request):
    form = ResetPasswordForm()

    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            requesting_user = form.user_cache
            request.session['confirmation_sent_to'] = requesting_user.pk

            mail_subject = _("Confirm %(username)s password change "
                             "on %(forum_title)s forums")
            subject_formats = {'username': requesting_user.username,
                               'forum_title': settings.forum_name}
            mail_subject = mail_subject % subject_formats

            confirmation_token = make_password_reset_token(requesting_user)

            mail_user(
                request, requesting_user, mail_subject,
                'misago/emails/forgottenpassword/confirm',
                {'confirmation_token': confirmation_token})

            return redirect('misago:reset_password_confirmation_sent')

    return render(request, 'misago/forgottenpassword/request.html',
                  {'form': form})


@reset_view
def confirmation_sent(request):
    requesting_user_pk = request.session.get('confirmation_sent_to')
    if not requesting_user_pk:
        raise Http404()

    User = get_user_model()
    requesting_user = get_object_or_404(User.objects, pk=requesting_user_pk)

    return render(request, 'misago/forgottenpassword/confirmation_sent.html',
                  {'requesting_user': requesting_user})



class ResetStopped(Exception):
    pass


class ResetError(Exception):
    pass


@reset_view
def reset_password(request, user_id, token):
    User = get_user_model()
    requesting_user = get_object_or_404(User.objects, pk=user_id)

    try:
        if requesting_user.requires_activation_by_admin:
            message = _("%(username)s, administrator has to activate your "
                        "account before you will be able to request "
                        "new password.")
            message = message % {'username': requesting_user.username}
            raise ResetStopped(message)
        if requesting_user.requires_activation_by_user:
            message = _("%(username)s, you have to activate your account "
                        "before you will be able to request new password.")
            message = message % {'username': requesting_user.username}
            raise ResetStopped(message)
        if get_user_ban(requesting_user):
            message = _("%(username)s, your account is banned "
                        "and it's password can't be changed.")
            message = message % {'username': requesting_user.username}
            raise ResetError(message)
        if not is_password_reset_token_valid(requesting_user, token):
            message = _("%(username)s, your confirmation link is invalid. "
                        "Try again or request new confirmation message.")
            message = message % {'username': requesting_user.username}
            raise ResetError(message)
    except ResetStopped as e:
        messages.info(request, e.args[0])
        return redirect('misago:index')
    except ResetError as e:
        messages.error(request, e.args[0])
        return redirect('misago:request_password_reset')

    fake = Factory.create()
    new_password = ' '.join([fake.word() for x in xrange(4)])
    while len(new_password) < settings.password_length_min:
        new_password = '%s %s' % (new_password, fake.word())

    requesting_user.set_password(new_password)
    requesting_user.save(update_fields=['password'])

    mail_subject = _("New password on %(forum_title)s forums")
    mail_subject = mail_subject % {'forum_title': settings.forum_name}

    confirmation_token = make_password_reset_token(requesting_user)

    mail_user(
        request, requesting_user, mail_subject,
        'misago/emails/forgottenpassword/new',
        {'new_password': new_password})

    request.session['password_sent_to'] = requesting_user.pk
    return redirect('misago:request_password_new_sent')


@reset_view
def new_password_sent(request):
    requesting_user_pk = request.session.get('password_sent_to')
    if not requesting_user_pk:
        raise Http404()

    User = get_user_model()
    requesting_user = get_object_or_404(User.objects, pk=requesting_user_pk)

    return render(request, 'misago/forgottenpassword/password_sent.html',
                  {'requesting_user': requesting_user})
