from django.utils.translation import ugettext as _

from rest_framework import status
from rest_framework.response import Response

from misago.conf import settings
from misago.core.mail import mail_user

from misago.users.credentialchange import store_new_credential
from misago.users.forms.options import ChangeEmailForm


def change_email_endpoint(request, pk=None):
    form = ChangeEmailForm(request.data, user=request.user)
    if form.is_valid():
        token = store_new_credential(
            request, 'email', form.cleaned_data['new_email'])

        mail_subject = _("Confirm e-mail change on %(forum_name)s forums")
        mail_subject = mail_subject % {'forum_name': settings.forum_name}

        # swap address with new one so email is sent to new address
        request.user.email = form.cleaned_data['new_email']

        mail_user(request, request.user, mail_subject,
                  'misago/emails/change_email',
                  {'token': token})

        message = _("E-mail change confirmation link was sent to new address.")
        return Response({'detail': message})
    else:
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
