from django.contrib.auth import authenticate, get_user_model, login
from django.core.exceptions import PermissionDenied, ValidationError
from django.db import IntegrityError
from django.utils.translation import gettext as _
from django.views.decorators.csrf import csrf_protect
from rest_framework import status
from rest_framework.response import Response

from ... import captcha
from ....legal.models import Agreement
from ...forms.register import RegisterForm
from ...registration import (
    get_registration_result_json,
    save_user_agreements,
    send_welcome_email,
)
from ...setupnewuser import setup_new_user

User = get_user_model()


@csrf_protect
def create_endpoint(request):
    if request.settings.account_activation == "closed":
        raise PermissionDenied(_("New users registrations are currently closed."))

    request_data = request.data
    if not isinstance(request_data, dict):
        request_data = {}

    form = RegisterForm(
        request_data, request=request, agreements=Agreement.objects.get_agreements()
    )

    try:
        if form.is_valid():
            captcha.test_request(request)
    except ValidationError as e:
        form.add_error("captcha", e)

    if not form.is_valid():
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

    activation_kwargs = {}
    if request.settings.account_activation == "user":
        activation_kwargs = {"requires_activation": User.ACTIVATION_USER}
    elif request.settings.account_activation == "admin":
        activation_kwargs = {"requires_activation": User.ACTIVATION_ADMIN}

    try:
        new_user = User.objects.create_user(
            form.cleaned_data["username"],
            form.cleaned_data["email"],
            form.cleaned_data["password"],
            joined_from_ip=request.user_ip,
            **activation_kwargs
        )
    except IntegrityError:
        return Response(
            {"__all__": _("Please try resubmitting the form.")},
            status=status.HTTP_400_BAD_REQUEST,
        )

    setup_new_user(request.settings, new_user)
    save_user_agreements(new_user, form)
    send_welcome_email(request, new_user)

    if new_user.requires_activation == User.ACTIVATION_NONE:
        authenticated_user = authenticate(
            username=new_user.email, password=form.cleaned_data["password"]
        )
        login(request, authenticated_user)

    return Response(get_registration_result_json(new_user))
