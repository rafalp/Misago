from django.utils.translation import ugettext as _

from rest_framework import status
from rest_framework.response import Response

from misago.conf import settings
from misago.core.mail import mail_user

from ...credentialchange import store_new_credential
from ...forms.options import ChangePasswordForm


def change_password_endpoint(request, pk=None):
    form = ChangePasswordForm(request.data, user=request.user)
    if form.is_valid():
        token = store_new_credential(
            request, 'password', form.cleaned_data['new_password'])

        mail_subject = _("Confirm password change on %(forum_name)s forums")
        mail_subject = mail_subject % {'forum_name': settings.forum_name}

        mail_user(request, request.user, mail_subject,
                  'misago/emails/change_password',
                  {'token': token})

        return Response({'detail': _("Password change confirmation link "
                                     "was sent to your address.")})
    else:
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
