from django.utils.translation import gettext as _
from rest_framework import status
from rest_framework.response import Response

from ....core.mail import mail_user
from ...credentialchange import store_new_credential
from ...serializers import ChangeEmailSerializer


def change_email_endpoint(request, pk=None):
    serializer = ChangeEmailSerializer(
        data=request.data, context={"user": request.user}
    )

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    token = store_new_credential(
        request, "email", serializer.validated_data["new_email"]
    )

    mail_subject = _("Confirm e-mail change on %(forum_name)s forums")
    mail_subject = mail_subject % {"forum_name": request.settings.forum_name}

    # swap address with new one so email is sent to new address
    request.user.email = serializer.validated_data["new_email"]

    mail_user(
        request.user,
        mail_subject,
        "misago/emails/change_email",
        context={"settings": request.settings, "token": token},
    )

    message = _("E-mail change confirmation link was sent to new address.")
    return Response({"detail": message})
