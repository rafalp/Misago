from rest_framework import status
from rest_framework.response import Response

from django.utils.translation import ugettext as _

from misago.conf import settings
from misago.core.mail import mail_user
from misago.users.credentialchange import store_new_credential
from misago.users.serializers import ChangePasswordSerializer


def change_password_endpoint(request, pk=None):
    serializer = ChangePasswordSerializer(
        data=request.data,
        context={'user': request.user},
    )

    if serializer.is_valid():
        token = store_new_credential(
            request, 'password', serializer.validated_data['new_password']
        )

        mail_subject = _("Confirm password change on %(forum_name)s forums")
        mail_subject = mail_subject % {'forum_name': settings.forum_name}

        mail_user(
            request, request.user, mail_subject, 'misago/emails/change_password', {'token': token}
        )

        return Response({
            'detail': _("Password change confirmation link was sent to your address.")
        })
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
