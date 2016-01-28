from django.contrib.auth import update_session_auth_hash
from django.core.urlresolvers import reverse
from django.db import IntegrityError
from django.shortcuts import render
from django.utils.translation import ugettext as _

from misago.users.credentialchange import read_new_credential
from misago.users.decorators import deny_guests


@deny_guests
def index(request, *args, **kwargs):
    request.frontend_context.update({
        'USERNAME_CHANGES_API': reverse('misago:api:usernamechange-list'),

        'USER_OPTIONS': [
            {
                'name': _("Forum options"),
                'icon': 'settings',
                'component': 'forum-options',
            },
            {
                'name': _("Change username"),
                'icon': 'card_membership',
                'component': 'change-username',
            },
            {
                'name': _("Change sign-in credentials"),
                'icon': 'vpn_key',
                'component': 'sign-in-credentials',
            },
        ]
    });

    return render(request, 'misago/options/noscript.html')


class ChangeError(Exception):
    pass


def confirm_change_view(f):
    @deny_guests
    def decorator(request, token):
        try:
            return f(request, token)
        except ChangeError as e:
            return render(request, 'misago/options/credentials_error.html',
                status=400)
    return decorator


@confirm_change_view
def confirm_email_change(request, token):
    new_credential = read_new_credential(request, 'email', token)
    if not new_credential:
        raise ChangeError()

    try:
        request.user.set_email(new_credential)
        request.user.save(update_fields=['email', 'email_hash'])
    except IntegrityError:
        raise ChangeError()

    message = _("%(user)s, your e-mail has been changed.")
    return render(request, 'misago/options/credentials_changed.html', {
            'message': message % {'user': request.user.username},
        })


@confirm_change_view
def confirm_password_change(request, token):
    new_credential = read_new_credential(request, 'password', token)
    if not new_credential:
        raise ChangeError()

    request.user.set_password(new_credential)
    update_session_auth_hash(request, request.user)
    request.user.save(update_fields=['password'])

    message = _("%(user)s, your password has been changed.")
    return render(request, 'misago/options/credentials_changed.html', {
            'message': message % {'user': request.user.username},
        })
