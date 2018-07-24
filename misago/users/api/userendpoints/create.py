from rest_framework import status
from rest_framework.response import Response

from django.contrib.auth import authenticate, get_user_model, login
from django.core.exceptions import PermissionDenied, ValidationError
from django.db import IntegrityError
from django.utils.translation import ugettext as _
from django.views.decorators.csrf import csrf_protect

from misago.conf import settings
from misago.users import captcha
from misago.users.forms.register import RegisterForm
from misago.users.registration import get_registration_result_json, send_welcome_email


UserModel = get_user_model()


@csrf_protect
def create_endpoint(request):
    if settings.account_activation == 'closed':
        raise PermissionDenied(_("New users registrations are currently closed."))

    form = RegisterForm(request.data, request=request)

    try:
        if form.is_valid():
            captcha.test_request(request)
    except ValidationError as e:
        form.add_error('captcha', e)

    if not form.is_valid():
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

    activation_kwargs = {}
    if settings.account_activation == 'user':
        activation_kwargs = {'requires_activation': UserModel.ACTIVATION_USER}
    elif settings.account_activation == 'admin':
        activation_kwargs = {'requires_activation': UserModel.ACTIVATION_ADMIN}

    try:
        new_user = UserModel.objects.create_user(
            form.cleaned_data['username'],
            form.cleaned_data['email'],
            form.cleaned_data['password'],
            joined_from_ip=request.user_ip,
            set_default_avatar=True,
            **activation_kwargs
        )
    except IntegrityError:
        return Response(
            {
                '__all__': _("Please try resubmitting the form.")
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    send_welcome_email(request, new_user)

    if new_user.requires_activation == UserModel.ACTIVATION_NONE:
        authenticated_user = authenticate(
            username=new_user.email, password=form.cleaned_data['password']
        )
        login(request, authenticated_user)

    return Response(get_registration_result_json(new_user))
