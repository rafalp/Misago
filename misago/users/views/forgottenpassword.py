from django.contrib import messages
from django.contrib.auth import get_user_model
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import ugettext as _
from django.views.decorators.debug import sensitive_post_parameters

from misago.conf import settings
from misago.core.mail import mail_user
from misago.core.views import noscript

from misago.users.bans import get_user_ban
from misago.users.decorators import deny_authenticated, deny_banned_ips
from misago.users.forms.auth import ResetPasswordForm, SetNewPasswordForm
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
    return noscript(request, **{
        'title': _("Change forgotten password"),
        'message': _("To change forgotten password enable JavaScript."),
    })
    form = ResetPasswordForm()

    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            requesting_user = form.user_cache
            request.session['reset_password_link_sent_to'] = requesting_user.pk

            mail_subject = _("Change %(user)s password "
                             "on %(forum_title)s forums")
            subject_formats = {'user': requesting_user.username,
                               'forum_title': settings.forum_name}
            mail_subject = mail_subject % subject_formats

            confirmation_token = make_password_reset_token(requesting_user)

            mail_user(request, requesting_user, mail_subject,
                      'misago/emails/change_password_form_link',
                      {'confirmation_token': confirmation_token})

            return redirect('misago:reset_password_link_sent')

    return render(request, 'misago/forgottenpassword/request.html',
                  {'form': form})


@reset_view
def link_sent(request):
    requesting_user_pk = request.session.get('reset_password_link_sent_to')
    if not requesting_user_pk:
        raise Http404()

    User = get_user_model()
    requesting_user = get_object_or_404(User.objects, pk=requesting_user_pk)

    return render(request, 'misago/forgottenpassword/link_sent.html',
                  {'requesting_user': requesting_user})


class ResetStopped(Exception):
    pass


class ResetError(Exception):
    pass


@sensitive_post_parameters()
@reset_view
def reset_password_form(request, user_id, token):
    User = get_user_model()
    requesting_user = get_object_or_404(User.objects, pk=user_id)

    try:
        if requesting_user.requires_activation_by_admin:
            message = _("%(user)s, administrator has to activate your "
                        "account before you will be able to request "
                        "new password.")
            message = message % {'user': requesting_user.username}
            raise ResetStopped(message)
        if requesting_user.requires_activation_by_user:
            message = _("%(user)s, you have to activate your account "
                        "before you will be able to request new password.")
            message = message % {'user': requesting_user.username}
            raise ResetStopped(message)
        if get_user_ban(requesting_user):
            message = _("%(user)s, your account is banned "
                        "and it's password can't be changed.")
            message = message % {'user': requesting_user.username}
            raise ResetError(message)
        if not is_password_reset_token_valid(requesting_user, token):
            message = _("%(user)s, your link is invalid. "
                        "Try again or request new link.")
            message = message % {'user': requesting_user.username}
            raise ResetError(message)
    except ResetStopped as e:
        messages.info(request, e.args[0])
        return redirect('misago:index')
    except ResetError as e:
        messages.error(request, e.args[0])
        return redirect('misago:request_password_reset')

    form = SetNewPasswordForm()
    if request.method == 'POST':
        form = SetNewPasswordForm(request.POST)
        if form.is_valid():
            requesting_user.set_password(form.cleaned_data['new_password'])
            requesting_user.save(update_fields=['password'])

            message = _("%(user)s, your password has been changed.")
            message = message % {'user': requesting_user.username}
            messages.success(request, message)
            return redirect(settings.LOGIN_URL)

    return render(request, 'misago/forgottenpassword/reset_password_form.html',
                  {'requesting_user': requesting_user, 'form': form})
