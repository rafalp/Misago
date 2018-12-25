from django.core.exceptions import PermissionDenied
from django.utils.translation import gettext as _
from rest_framework import status
from rest_framework.response import Response

from ....core.utils import format_plaintext_for_html
from ...serializers import EditSignatureSerializer
from ...signatures import is_user_signature_valid, set_user_signature


def signature_endpoint(request):
    if not request.user_acl["can_have_signature"]:
        raise PermissionDenied(_("You don't have permission to change signature."))

    user = request.user

    if user.is_signature_locked:
        if user.signature_lock_user_message:
            reason = format_plaintext_for_html(user.signature_lock_user_message)
        else:
            reason = None

        return Response(
            {
                "detail": _("Your signature is locked. You can't change it."),
                "reason": reason,
            },
            status=status.HTTP_403_FORBIDDEN,
        )

    if request.method == "POST":
        return edit_signature(request, user)

    return get_signature_options(request.settings, user)


def get_signature_options(settings, user):
    options = {"signature": None, "limit": settings.signature_length_max}

    if user.signature:
        options["signature"] = {"plain": user.signature, "html": user.signature_parsed}

        if not is_user_signature_valid(user):
            # pylint: disable=unsupported-assignment-operation
            options["signature"]["html"] = None

    return Response(options)


def edit_signature(request, user):
    serializer = EditSignatureSerializer(
        user, data=request.data, context={"settings": request.settings}
    )
    if serializer.is_valid():
        signature = serializer.validated_data["signature"]
        set_user_signature(request, user, request.user_acl, signature)
        user.save(update_fields=["signature", "signature_parsed", "signature_checksum"])
        return get_signature_options(request.settings, user)

    return Response(
        {"detail": serializer.errors["non_field_errors"][0]},
        status=status.HTTP_400_BAD_REQUEST,
    )
