from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.utils.translation import ugettext as _

from rest_framework import status
from rest_framework.response import Response

from misago.conf import settings
from misago.core.mail import mail_user

from misago.users.forms.options import ChangeEmailForm
from misago.users.credentialchange import (store_new_credential,
                                           read_new_credential)


def change_email_endpoint(request, pk=None):
    if 'token' in request.data:
        return use_token(request, request.data['token'])
    else:
        return handle_form_submission(request)


def handle_form_submission(request):
    form = ChangeEmailForm(request.data, user=request.user)
    if form.is_valid():
        token = store_new_credential(
            request, 'email', form.cleaned_data['new_email'])

        mail_subject = _("Confirm e-mail change on %(forum_title)s forums")
        mail_subject = mail_subject % {'forum_title': settings.forum_name}

        # swap address with new one so email is sent to new address
        request.user.email = form.cleaned_data['new_email']

        mail_user(request, request.user, mail_subject,
                  'misago/emails/change_email',
                  {'token': token})

        message = _("E-mail change confirmation link was sent to new address.")
        return Response({'detail': message})
    else:
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)


def token_error_handler(f):
    def decorator(request, token):
        try:
            return f(request, token)
        except (ValueError, IntegrityError):
            message = _("E-mail change link has expired. Please try again.")
            return Response({'detail': message},
                            status=status.HTTP_400_BAD_REQUEST)

    return decorator


@token_error_handler
def use_token(request, token):
    new_email = read_new_credential(request, 'email', token)
    if new_email:
        request.user.set_email(new_email)
        request.user.save()
        return Response({'detail': _("Your e-mail has been changed.")})
    else:
        raise ValueError()
