from django.urls import reverse

from .pages import user_profile, users_list
from .serializers import AnonymousUserSerializer, AuthenticatedUserSerializer
from .usersmenus import get_users_menus


def user_links(request):
    if request.include_frontend_context:
        request.frontend_context.update(
            {
                "REQUEST_ACTIVATION_URL": reverse("misago:request-activation"),
                "FORGOTTEN_PASSWORD_URL": reverse("misago:forgotten-password"),
                "BANNED_URL": reverse("misago:banned"),
                "USERS_LIST_URL": reverse("misago:users"),
                "AUTH_API": reverse("misago:api:auth"),
                "AUTH_CRITERIA_API": reverse("misago:api:auth-criteria"),
                "USERS_API": reverse("misago:api:user-list"),
                "CAPTCHA_API": reverse("misago:api:captcha-question"),
                "USERNAME_CHANGES_API": reverse("misago:api:usernamechange-list"),
                "MENTION_API": reverse("misago:api:mention-suggestions"),
            }
        )

    return {
        "USERS_LIST_URL": users_list.get_default_link(),
        "USER_PROFILE_URL": user_profile.get_default_link(),
    }


def preload_user_json(request):
    if not request.include_frontend_context:
        return {}

    request.frontend_context.update(
        {"isAuthenticated": bool(request.user.is_authenticated)}
    )

    if request.user.is_authenticated:
        serializer = AuthenticatedUserSerializer
    else:
        serializer = AnonymousUserSerializer

    serialized_user = serializer(request.user, context={"acl": request.user_acl}).data
    request.frontend_context["user"] = serialized_user

    request.frontend_context.update(get_users_menus(request))

    return {}
