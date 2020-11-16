from django.contrib.auth import logout
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext as _
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Agreement
from .utils import save_user_agreement_acceptance


@api_view(["POST"])
def submit_agreement(request, pk):
    agreement = get_object_or_404(Agreement, is_active=True, pk=pk)

    if agreement.id in request.user.agreements:
        raise PermissionDenied(_("You have already accepted this agreement."))

    if request.data.get("accept") is True:
        save_user_agreement_acceptance(request.user, agreement, commit=True)
    elif request.data.get("accept") is False:
        if not request.user.is_staff:
            request.user.mark_for_delete()
            logout(request)
    else:
        raise PermissionDenied(_("You need to submit a valid choice."))

    return Response({"detail": "ok"})
