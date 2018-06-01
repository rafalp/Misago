from rest_framework.response import Response

from django.contrib.auth import authenticate, get_user_model, login
from django.core.exceptions import PermissionDenied, ValidationError
from django.db import IntegrityError
from django.utils.translation import ugettext as _
from django.views.decorators.csrf import csrf_protect

from misago.conf import settings
from misago.core.exceptions import Banned
from misago.users.bans import get_ip_ban
from misago.users.serializers import RegisterUserSerializer
from misago.users.registration import get_registration_result_json, send_welcome_email


UserModel = get_user_model()


@csrf_protect
def create_endpoint(request):
    if settings.account_activation == 'closed':
        raise PermissionDenied(_("New users registrations are currently closed."))

    ban = get_ip_ban(request.user_ip, registration_only=True)
    if ban:
        raise Banned(ban)

    serializer = RegisterUserSerializer(
        data=request.data,
        context={'request': request},
    )

    serializer.is_valid(raise_exception=True)

    activation_kwargs = {}
    if settings.account_activation == 'user':
        activation_kwargs = {'requires_activation': UserModel.ACTIVATION_USER}
    elif settings.account_activation == 'admin':
        activation_kwargs = {'requires_activation': UserModel.ACTIVATION_ADMIN}

    try:
        new_user = UserModel.objects.create_user(
            serializer.validated_data['username'],
            serializer.validated_data['email'],
            serializer.validated_data['password'],
            joined_from_ip=request.user_ip,
            set_default_avatar=True,
            **activation_kwargs
        )
    except IntegrityError:
        return Response(
            {
                'detail': _("Please try resubmitting the form."),
            },
            status=400,
        )

    send_welcome_email(request, new_user)

    if not new_user.requires_activation == 'none':
        authenticated_user = authenticate(
            username=new_user.email,
            password=serializer.validated_data['password'],
        )
        login(request, authenticated_user)

    return Response(get_registration_result_json(new_user))
