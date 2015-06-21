from django.contrib.auth import update_session_auth_hash
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _

from rest_framework import status
from rest_framework.response import Response

from misago.conf import settings
from misago.core.mail import mail_user

from misago.users.forms.options import ChangePasswordForm
from misago.users.credentialchange import (store_new_credential,
                                           read_new_credential)


def change_password_endpoint(request, pk=None):
    if 'token' in request.data:
        return use_token(request, request.data['token'])
    else:
        return handle_form_submission(request)


def handle_form_submission(request):
    form = ChangePasswordForm(request.data, user=request.user)
    if form.is_valid():
        token = store_new_credential(
            request, 'password', form.cleaned_data['new_password'])

        mail_subject = _("Confirm password change on %(forum_title)s forums")
        mail_subject = mail_subject % {'forum_title': settings.forum_name}

        mail_user(request, request.user, mail_subject,
                  'misago/emails/change_password',
                  {'token': token})

        return Response({'detail': _("Password change confirmation link "
                                     "was sent to your address.")})
    else:
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)


def token_error_handler(f):
    def decorator(request, token):
        try:
            return f(request, token)
        except ValueError:
            message = _("Password change link has expired. Please try again.")
            return Response({'detail': message},
                            status=status.HTTP_400_BAD_REQUEST)

    return decorator


@token_error_handler
def use_token(request, token):
    new_password = read_new_credential(request, 'password', token)
    if new_password:
        request.user.set_password(new_password)
        request.user.save()
        update_session_auth_hash(request, request.user)
        return Response({'detail': _("Your password has been changed.")})
    else:
        raise ValueError()
