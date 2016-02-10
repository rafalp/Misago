from django.core.urlresolvers import reverse

from misago.users.pages import usercp, users_list, user_profile
from misago.users.serializers import (
    AuthenticatedUserSerializer, AnonymousUserSerializer)


def user_links(request):
    request.frontend_context.update({
        'REQUEST_ACTIVATION_URL': reverse('misago:request_activation'),
        'FORGOTTEN_PASSWORD_URL': reverse('misago:forgotten_password'),

        'BANNED_URL': reverse('misago:banned'),

        'USERCP_URL': reverse('misago:options'),
        'USERS_LIST_URL': reverse('misago:users'),

        'AUTH_API': reverse('misago:api:auth'),
        'USERS_API': reverse('misago:api:user-list'),

        'CAPTCHA_API_URL': reverse('misago:api:captcha_question'),
        'USERNAME_CHANGES_API': reverse('misago:api:usernamechange-list'),
    })

    return {
        'USERCP_URL': usercp.get_default_link(),
        'USERS_LIST_URL': users_list.get_default_link(),
        'USER_PROFILE_URL': user_profile.get_default_link(),
    }


def preload_user_json(request):
    request.frontend_context.update({
        'isAuthenticated': request.user.is_authenticated(),
    })

    if request.user.is_authenticated():
        request.frontend_context.update({
            'user': AuthenticatedUserSerializer(request.user).data
        })
    else:
        request.frontend_context.update({
            'user': AnonymousUserSerializer(request.user).data
        })

    return {}
