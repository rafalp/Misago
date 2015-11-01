from django.contrib import auth
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _
from django.views.decorators.csrf import csrf_protect

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from misago.conf import settings
from misago.core.mail import mail_user

from misago.users.forms.auth import (AuthenticationForm, ResendActivationForm,
                                     ResetPasswordForm)
from misago.users.rest_permissions import UnbannedAnonOnly, UnbannedOnly
from misago.users.serializers import (AuthenticatedUserSerializer,
                                      AnonymousUserSerializer)
from misago.users.tokens import (make_activation_token,
                                 is_activation_token_valid,
                                 make_password_change_token,
                                 is_password_change_token_valid)
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

        mail_subject = _("Activate %(user)s account "
                         "on %(forum_title)s forums")
        subject_formats = {'user': requesting_user.username,
                           'forum_title': settings.forum_name}
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
POST /auth/activate-account/ with CSRF token, user ID and activation token
will activate account
"""
@api_view(['POST'])
@permission_classes((UnbannedAnonOnly,))
@csrf_protect
def activate_account(request, user_id, token):
    User = auth.get_user_model()

    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        message = _("Activation link is invalid. Please try again.")
        return Response({'detail': message}, status=status.HTTP_400_BAD_REQUEST)

    if not is_activation_token_valid(user, token):
        message = _("Activation link is invalid. Please try again.")
        return Response({'detail': message},
                        status=status.HTTP_400_BAD_REQUEST)

    form = ResendActivationForm()
    try:
        form.confirm_user_not_banned(user)
    except ValidationError:
        message = _("Activation link has expired. Please request new one.")
        return Response({'detail': message},
                        status=status.HTTP_400_BAD_REQUEST)

    try:
        form.confirm_can_be_activated(user)
    except ValidationError as e:
        return Response({'detail': e.messages[0]},
                        status=status.HTTP_400_BAD_REQUEST)

    user.requires_activation = False
    user.save(update_fields=['requires_activation'])

    return Response({
            'username': user.username
        })


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

        mail_subject = _("Change %(user)s password on %(forum_title)s forums")
        subject_formats = {'user': requesting_user.username,
                           'forum_title': settings.forum_name}
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
GET /auth/change-password/user/token/ will validate change password link
POST /auth/change-password/user/token/ with CSRF and new password
will change forgotten password
"""
@api_view(['GET', 'POST'])
@permission_classes((UnbannedOnly,))
@csrf_protect
def change_forgotten_password(request, user_id, token):
    User = auth.get_user_model()
    invalid_message = _("Form link is invalid. Please try again.")

    try:
        user = User.objects.get(pk=user_id)
        if request.user.is_authenticated() and request.user.id != user.id:
            raise User.DoesNotExist()
    except User.DoesNotExist:
        return Response({'detail': invalid_message},
                        status=status.HTTP_400_BAD_REQUEST)

    if not is_password_change_token_valid(user, token):
        return Response({'detail': invalid_message},
                        status=status.HTTP_400_BAD_REQUEST)

    try:
        form = ResetPasswordForm()
        form.confirm_allowed(user)
    except ValidationError:
        message = _("Your link has expired. Please request new one.")
        return Response({'detail': message},
                        status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'POST':
        return process_forgotten_password_form(request, user)
    else:
        return Response({
                'username': user.username,
                'email': user.email
            })


def process_forgotten_password_form(request, user):
    new_password = request.data.get('password', '').strip()
    try:
        validate_password(new_password)
        user.set_password(new_password)
        user.save()
    except ValidationError as e:
        return Response({'detail': e.messages[0]},
                        status=status.HTTP_400_BAD_REQUEST)
    return Response({
            'username': user.username
        })
