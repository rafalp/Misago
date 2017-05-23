from rest_framework import status
from rest_framework.response import Response

from django.utils.translation import ugettext as _

from misago.conf import settings
from misago.core.mail import mail_user
from misago.users.credentialchange import store_new_credential
from misago.users.serializers import ChangeEmailSerializer


def change_email_endpoint(request, pk=None):
    serializer = ChangeEmailSerializer(
        data=request.data,
        context={'user': request.user},
    )

    if serializer.is_valid():
        token = store_new_credential(request, 'email', serializer.validated_data['new_email'])

        mail_subject = _("Confirm e-mail change on %(forum_name)s forums")
        mail_subject = mail_subject % {'forum_name': settings.forum_name}

        # swap address with new one so email is sent to new address
        request.user.email = serializer.validated_data['new_email']

        mail_user(
            request, request.user, mail_subject, 'misago/emails/change_email', {'token': token}
        )

        message = _("E-mail change confirmation link was sent to new address.")
        return Response({'detail': message})
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
