from django.urls import reverse

from .pages import user_profile, usercp, users_list
from .serializers import AnonymousUserSerializer, AuthenticatedUserSerializer


def user_links(request):
    if request.include_frontend_context:
        request.frontend_context.update({
            'REQUEST_ACTIVATION_URL': reverse('misago:request-activation'),
            'FORGOTTEN_PASSWORD_URL': reverse('misago:forgotten-password'),
            'BANNED_URL': reverse('misago:banned'),
            'USERCP_URL': reverse('misago:options'),
            'USERS_LIST_URL': reverse('misago:users'),
            'AUTH_API': reverse('misago:api:auth'),
            'AUTH_CRITERIA_API': reverse('misago:api:auth-criteria'),
            'USERS_API': reverse('misago:api:user-list'),
            'CAPTCHA_API': reverse('misago:api:captcha-question'),
            'USERNAME_CHANGES_API': reverse('misago:api:usernamechange-list'),
        })

    return {
        'USERCP_URL': usercp.get_default_link(),
        'USERS_LIST_URL': users_list.get_default_link(),
        'USER_PROFILE_URL': user_profile.get_default_link(),
    }


def preload_user_json(request):
    if not request.include_frontend_context:
        return {}

    request.frontend_context.update({
        'isAuthenticated': bool(request.user.is_authenticated),
    })

    if request.user.is_authenticated:
        request.frontend_context.update({'user': AuthenticatedUserSerializer(request.user).data})
    else:
        request.frontend_context.update({'user': AnonymousUserSerializer(request.user).data})

    return {}
