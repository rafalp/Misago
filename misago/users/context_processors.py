from .pages import user_profile, usercp, users_list
from .serializers import AnonymousUserSerializer, AuthenticatedUserSerializer


def user_links(request):
    return {
        'USERCP_URL': usercp.get_default_link(),
        'USERS_LIST_URL': users_list.get_default_link(),
        'USER_PROFILE_URL': user_profile.get_default_link(),
    }


def preload_user_json(request):
    if not request.include_frontend_context:
        return {}

    request.frontend_context['auth'].update({
        'id': request.user.id,
        'isAnonymous': bool(request.user.is_anonymous),
        'isAuthenticated': bool(request.user.is_authenticated),
    })

    if request.user.is_authenticated:
        request.frontend_context['store'].update({
            'auth': AuthenticatedUserSerializer(request.user).data,
        })
    else:
        request.frontend_context['store'].update({
            'auth': AnonymousUserSerializer(request.user).data,
        })

    return {}
