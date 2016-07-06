from django.contrib import auth
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _
from django.views.decorators.csrf import csrf_protect

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from misago.conf import settings
from misago.core.mail import mail_user
from misago.users.bans import get_user_ban
from misago.users.forms.auth import AuthenticationForm, ResendActivationForm, ResetPasswordForm
from misago.users.rest_permissions import UnbannedAnonOnly, UnbannedOnly
from misago.users.serializers import AnonymousUserSerializer, AuthenticatedUserSerializer
from misago.users.tokens import is_password_change_token_valid, make_activation_token, make_password_change_token
from misago.users.validators import validate_password


def gateway(request):
    if request.method == 'POST':
        return login(request)
    else:
        return session_user(request)


"""
POST /auth/ with CSRF, username and password
will attempt to authenticate new user
"""
@api_view(['POST'])
@permission_classes((UnbannedAnonOnly,))
@csrf_protect
def login(request):
    form = AuthenticationForm(request, data=request.data)
    if form.is_valid():
        auth.login(request, form.user_cache)
        return Response(AuthenticatedUserSerializer(form.user_cache).data)
    else:
        return Response(form.get_errors_dict(),
                        status=status.HTTP_400_BAD_REQUEST)


"""
GET /auth/ will return current auth user, either User or AnonymousUser
"""
@api_view()
def session_user(request):
    if request.user.is_authenticated():
        UserSerializer = AuthenticatedUserSerializer
    else:
        UserSerializer = AnonymousUserSerializer

    return Response(UserSerializer(request.user).data)


"""
POST /auth/send-activation/ with CSRF token and email
will mail account activation link to requester
"""
@api_view(['POST'])
@permission_classes((UnbannedAnonOnly,))
@csrf_protect
def send_activation(request):
    form = ResendActivationForm(request.data)
    if form.is_valid():
        requesting_user = form.user_cache

        mail_subject = _("Activate %(user)s account on %(forum_name)s forums")
        subject_formats = {
            'user': requesting_user.username,
            'forum_name': settings.forum_name,
        }
        mail_subject = mail_subject % subject_formats

        mail_user(request, requesting_user, mail_subject,
                  'misago/emails/activation/by_user',
                  {'activation_token': make_activation_token(requesting_user)})

        return Response({
                'username': form.user_cache.username,
                'email': form.user_cache.email
            })
    else:
        return Response(form.get_errors_dict(),
                        status=status.HTTP_400_BAD_REQUEST)


"""
POST /auth/send-password-form/ with CSRF token and email
will mail change password form link to requester
"""
@api_view(['POST'])
@permission_classes((UnbannedOnly,))
@csrf_protect
def send_password_form(request):
    form = ResetPasswordForm(request.data)
    if form.is_valid():
        requesting_user = form.user_cache

        mail_subject = _("Change %(user)s password on %(forum_name)s forums")
        subject_formats = {
            'user': requesting_user.username,
            'forum_name': settings.forum_name,
        }
        mail_subject = mail_subject % subject_formats

        confirmation_token = make_password_change_token(requesting_user)

        mail_user(request, requesting_user, mail_subject,
                  'misago/emails/change_password_form_link',
                  {'confirmation_token': confirmation_token})

        return Response({
                'username': form.user_cache.username,
                'email': form.user_cache.email
            })
    else:
        return Response(form.get_errors_dict(),
                        status=status.HTTP_400_BAD_REQUEST)


"""
POST /auth/change-password/user/token/ with CSRF and new password
will change forgotten password
"""
class PasswordChangeFailed(Exception):
    pass


@api_view(['POST'])
@permission_classes((UnbannedOnly,))
@csrf_protect
def change_forgotten_password(request, pk, token):
    User = auth.get_user_model()

    invalid_message = _("Form link is invalid. Please try again.")
    expired_message = _("Your link has expired. Please request new one.")

    try:
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise PasswordChangeFailed(invalid_message)

        if request.user.is_authenticated() and request.user.id != user.id:
            raise PasswordChangeFailed(invalid_message)
        if not is_password_change_token_valid(user, token):
            raise PasswordChangeFailed(invalid_message)

        if user.requires_activation:
            raise PasswordChangeFailed(expired_message)
        if get_user_ban(user):
            raise PasswordChangeFailed(expired_message)
    except PasswordChangeFailed as e:
        return Response({
                'detail': e.args[0]
            }, status=status.HTTP_400_BAD_REQUEST)

    try:
        new_password = request.data.get('password', '').strip()
        validate_password(new_password)
        user.set_password(new_password)
        user.save()
    except ValidationError as e:
        return Response({
                'detail': e.messages[0]
            }, status=status.HTTP_400_BAD_REQUEST)

    return Response({
            'username': user.username
        })
