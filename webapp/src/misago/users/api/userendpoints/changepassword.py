from django.utils.translation import gettext as _
from rest_framework import status
from rest_framework.response import Response

from ....core.mail import mail_user
from ...credentialchange import store_new_credential
from ...serializers import ChangePasswordSerializer


def change_password_endpoint(request, pk=None):
    serializer = ChangePasswordSerializer(
        data=request.data, context={"user": request.user}
    )

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    token = store_new_credential(
        request, "password", serializer.validated_data["new_password"]
    )

    mail_subject = _("Confirm password change on %(forum_name)s forums")
    mail_subject = mail_subject % {"forum_name": request.settings.forum_name}

    mail_user(
        request.user,
        mail_subject,
        "misago/emails/change_password",
        context={"settings": request.settings, "token": token},
    )

    return Response(
        {"detail": _("Password change confirmation link was sent to your address.")}
    )
