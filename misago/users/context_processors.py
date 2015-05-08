from misago.users.serializers import (AuthenticatedUserSerializer,
                                      AnonymousUserSerializer)
from misago.users.sites import usercp, users_list, user_profile


def sites_links(request):
    return {
        'USERCP_URL': usercp.get_default_link(),
        'USERS_LIST_URL': users_list.get_default_link(),
        'USER_PROFILE_URL': user_profile.get_default_link(),
    }


def preload_user_json(request):
    request.preloaded_ember_data.update({
        'isAuthenticated': request.user.is_authenticated(),
    })

    if request.user.is_authenticated():
        request.preloaded_ember_data.update({
            'user': AuthenticatedUserSerializer(request.user).data
        })
    else:
        request.preloaded_ember_data.update({
            'user': AnonymousUserSerializer(request.user).data
        })

    return {}
