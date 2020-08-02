from django.contrib.auth import get_user_model

from ..users.setupnewuser import setup_new_user

User = get_user_model()


def get_or_create_user(request, user_data):
    try:
        return User.objects.get(sso_id=user_data["id"])
    except User.DoesNotExist:
        try:
            return User.objects.get(email=user_data["email"])
        except User.DoesNotExist:
            username = User.objects.prepare_new_username(user_data["username"])
            user = User.objects.create_user(
                username,
                user_data["email"],
                is_active=user_data.get("is_active", True),
                sso_id=user_data["id"],
            )
            user.update_acl_key()
            setup_new_user(request.settings, user)
            return user


def user_needs_updating(user, user_data):
    return any(
        (
            user.username != user_data["username"],
            user.email != user_data["email"],
            user.is_active != user_data.get("is_active", user.is_active),
        )
    )


def update_user(user, user_data):
    if user.username != user_data["username"]:
        user.set_username(user_data["username"])
    if user.email != user_data["email"]:
        user.set_email(user_data["email"])
    if user.is_active != user_data.get("is_active", user.is_active):
        user.is_active = user_data["is_active"]
    user.save()
