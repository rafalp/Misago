from .audittrail import create_user_audit_trail
from .avatars import set_default_avatar
from .models import User


def setup_new_user(settings, user):
    set_default_subscription_options(settings, user)

    set_default_avatar(
        user, settings.default_avatar, settings.default_gravatar_fallback
    )

    if user.joined_from_ip:
        create_user_audit_trail(user, user.joined_from_ip, user)


SUBSCRIPTION_CHOICES = {
    "no": User.SUBSCRIPTION_NONE,
    "watch": User.SUBSCRIPTION_NOTIFY,
    "watch_email": User.SUBSCRIPTION_ALL,
}


def set_default_subscription_options(settings, user):
    started_threads = SUBSCRIPTION_CHOICES[settings.subscribe_start]
    user.subscribe_to_started_threads = started_threads

    replied_threads = SUBSCRIPTION_CHOICES[settings.subscribe_reply]
    user.subscribe_to_replied_threads = replied_threads
