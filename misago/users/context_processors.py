from misago.users.pages import usercp, users_list, user_profile
from misago.users.serializers import (
    AuthenticatedUserSerializer, AnonymousUserSerializer)


def sites_links(request):
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
