from .audittrail import create_user_audit_trail
from .avatars import set_default_avatar, set_default_avatar_from_url
from .models import User


def setup_new_user(settings, user, *, avatar_url=None):
    set_default_subscription_options(settings, user)
    set_default_notifications_options(settings, user)

    if avatar_url:
        set_default_avatar_from_url(user, avatar_url)
    else:
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

    user.save(
        update_fields=["subscribe_to_replied_threads", "subscribe_to_replied_threads"]
    )


def set_default_notifications_options(settings, user: User):
    user.watch_started_threads = settings.watch_started_threads
    user.watch_replied_threads = settings.watch_replied_threads
    user.watch_new_private_threads_by_followed = (
        settings.watch_new_private_threads_by_followed
    )
    user.watch_new_private_threads_by_other_users = (
        settings.watch_new_private_threads_by_other_users
    )
    user.notify_new_private_threads_by_followed = (
        settings.notify_new_private_threads_by_followed
    )
    user.notify_new_private_threads_by_other_users = (
        settings.notify_new_private_threads_by_other_users
    )

    user.save(
        update_fields=[
            "watch_started_threads",
            "watch_replied_threads",
            "watch_new_private_threads_by_followed",
            "watch_new_private_threads_by_other_users",
            "notify_new_private_threads_by_followed",
            "notify_new_private_threads_by_other_users",
        ]
    )
