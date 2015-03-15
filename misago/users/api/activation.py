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
from misago.users.forms.auth import ResendActivationForm
from misago.users.tokens import (make_activation_token,
                                 is_activation_token_valid)
from misago.users.validators import validate_password


def activation_api_view(f):
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

            if not is_activation_token_valid(user, kwargs['token']):
                message = _("Your link is invalid. Please try again.")
                return Response({'detail': message},
                                status=status.HTTP_404_NOT_FOUND)

            form = ResendActivationForm()
            try:
                form.confirm_user_not_banned(user)
            except ValidationError:
                message = _("Your link has expired. Please request new one.")
                return Response({'detail': message},
                                status=status.HTTP_404_NOT_FOUND)

            try:
                form.confirm_can_be_activated(user)
            except ValidationError as e:
                return Response({'detail': e.messages[0]},
                                status=status.HTTP_404_NOT_FOUND)

        return f(request, *args, **kwargs)
    return decorator


@activation_api_view
def send_link(request):
    form = ResendActivationForm(request.DATA)
    if form.is_valid():
        requesting_user = form.user_cache

        mail_subject = _("Change %(user)s password "
                         "on %(forum_title)s forums")
        subject_formats = {'user': requesting_user.username,
                           'forum_title': settings.forum_name}
        mail_subject = mail_subject % subject_formats

        confirmation_token = make_activation_token(requesting_user)

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


@activation_api_view
def validate_token(request, user, token):
    user.requires_activation = False
    user.save(update_fields=['requires_activation'])

    message = _("%(user)s, your account has been activated")
    return Response({
        'detail': message % {'user': user.username}
    })
