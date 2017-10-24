from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from django.contrib import auth
from django.utils.translation import ugettext as _
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import get_object_or_404

from misago.conf import settings
from misago.core.mail import mail_user
from misago.users.serializers import (
    AnonymousUserSerializer, AuthenticatedUserSerializer, LoginSerializer,
    ResendActivationSerializer, SendPasswordFormSerializer, ChangePasswordSerializer)
from misago.users.tokens import (
    make_activation_token, make_password_change_token)

from .rest_permissions import UnbannedAnonOnly, UnbannedOnly


UserModel = auth.get_user_model()


def gateway(request):
    if request.method == 'POST':
        return login(request)
    else:
        return session_user(request)


@api_view(['POST'])
@permission_classes((UnbannedAnonOnly, ))
@csrf_protect
def login(request):
    """
    POST /auth/ with CSRF, username and password
    will attempt to authenticate new user
    """
    serializer = LoginSerializer(request, data=request.data)
    serializer.is_valid(raise_exception=True)

    user = serializer.validated_data['user']
    auth.login(request, user)

    return Response(
        AuthenticatedUserSerializer(user).data,
    )


@api_view()
def session_user(request):
    """GET /auth/ will return current auth user, either User or AnonymousUser"""
    if request.user.is_authenticated:
        UserSerializer = AuthenticatedUserSerializer
    else:
        UserSerializer = AnonymousUserSerializer

    return Response(UserSerializer(request.user).data)


@api_view(['GET'])
def get_requirements(request):
    """GET /auth/requirements/ will return password and username requirements"""
    requirements = {
        'username': {
            'min_length': settings.username_length_min,
            'max_length': settings.username_length_max,
        },
        'password': [],
    }

    for validator in settings.AUTH_PASSWORD_VALIDATORS:
        validator_dict = {'name': validator['NAME'].split('.')[-1]}
        validator_dict.update(validator.get('OPTIONS', {}))
        requirements['password'].append(validator_dict)

    return Response(requirements)


@api_view(['POST'])
@permission_classes((UnbannedAnonOnly, ))
@csrf_protect
def send_activation(request):
    """
    POST /auth/send-activation/ with CSRF token and email
    will mail account activation link to requester
    """
    serializer = ResendActivationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.raise_if_banned()

    user = serializer.validated_data['user']

    mail_subject = _("Activate %(user)s account on %(forum_name)s forums") % {
        'user': user.username,
        'forum_name': settings.forum_name,
    }

    mail_user(
        request,
        user,
        mail_subject,
        'misago/emails/activation/by_user',
        {
            'activation_token': make_activation_token(user),
        },
    )

    return Response({
        'username': user.username,
        'email': user.email,
    })


@api_view(['POST'])
@permission_classes((UnbannedOnly, ))
@csrf_protect
def send_password_form(request):
    """
    POST /auth/send-password-form/ with CSRF token and email
    will mail change password form link to requester
    """
    serializer = SendPasswordFormSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.raise_if_banned()

    user = serializer.validated_data['user']

    mail_subject = _("Change %(user)s password on %(forum_name)s forums") % {
        'user': user.username,
        'forum_name': settings.forum_name,
    }

    confirmation_token = make_password_change_token(user)

    mail_user(
        request,
        user,
        mail_subject,
        'misago/emails/change_password_form_link',
        {
            'confirmation_token': confirmation_token,
        },
    )

    return Response({
        'username': user.username,
        'email': user.email,
    })


class PasswordChangeFailed(Exception):
    pass


@api_view(['POST'])
@permission_classes((UnbannedOnly, ))
@csrf_protect
def change_forgotten_password(request, pk):
    """
    POST /auth/change-password/user/ with CSRF and new password
    will change forgotten password
    """
    user = get_object_or_404(UserModel, pk=pk, is_active=True)
    serializer = ChangePasswordSerializer(user, data=request.data)
    serializer.is_valid(raise_exception=True)

    serializer.save()

    return Response({'username': user.username})
