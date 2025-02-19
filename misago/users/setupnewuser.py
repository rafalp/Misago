from .audittrail import create_user_audit_trail
from .avatars import set_default_avatar, set_default_avatar_from_url
from .models import User


def setup_new_user(settings, user, *, avatar_url=None):
    set_default_notifications_options(settings, user)

    if avatar_url:
        set_default_avatar_from_url(user, avatar_url)
    else:
        set_default_avatar(
            user, settings.default_avatar, settings.default_gravatar_fallback
        )

    if user.joined_from_ip:
        create_user_audit_trail(user, user.joined_from_ip, user)


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
