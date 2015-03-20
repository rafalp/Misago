from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext as _
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from misago.conf import settings
from misago.core.mail import mail_user

from misago.users.decorators import deny_authenticated, deny_banned_ips
from misago.users.forms.auth import ResetPasswordForm
from misago.users.tokens import (make_password_change_token,
                                 is_password_change_token_valid)
from misago.users.validators import validate_password


def password_api_view(f):
    @sensitive_post_parameters()
    @api_view(['POST'])
    @never_cache
    @deny_authenticated
    @csrf_protect
    @deny_banned_ips
    def decorator(request, *args, **kwargs):
        if 'user_id' in kwargs:
            User = get_user_model()
            user = get_object_or_404(User.objects, pk=kwargs.pop('user_id'))
            kwargs['user'] = user

            if not is_password_change_token_valid(user, kwargs['token']):
                message = _("Your link is invalid. Please try again.")
                return Response({'detail': message},
                                status=status.HTTP_404_NOT_FOUND)

            try:
                form = ResetPasswordForm()
                form.confirm_allowed(user)
            except ValidationError:
                message = _("Your link has expired. Please request new one.")
                return Response({'detail': message},
                                status=status.HTTP_404_NOT_FOUND)

        return f(request, *args, **kwargs)
    return decorator


@password_api_view
def send_link(request):
    form = ResetPasswordForm(request.DATA)
    if form.is_valid():
        requesting_user = form.user_cache

        mail_subject = _("Change %(user)s password "
                         "on %(forum_title)s forums")
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


@password_api_view
def validate_token(request, user, token):
    return Response({
        'user_id': user.id,
        'token': token,
        'username': user.username
    })


@password_api_view
def change_password(request, user, token):
    new_password = request.DATA.get('password', '').strip()

    try:
        validate_password(new_password)
        user.set_password(new_password)
        user.save()
    except ValidationError as e:
        return Response({'detail': e.messages[0]},
                        status=status.HTTP_400_BAD_REQUEST)

    return Response({'detail': 'ok'})
