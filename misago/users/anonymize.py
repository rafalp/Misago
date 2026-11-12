from typing import Any

from django.contrib.auth import get_user_model

from ..categories.utils import update_usernames as catetories_update_usernames
from ..core.utils import slugify
from ..legal.utils import update_usernames as legal_update_usernames
from ..notifications.utils import update_actor_name
from ..threads.utils import anonymize_user_in_likes, anonymize_user_in_thread_events
from ..threads.utils import update_usernames as threads_update_usernames
from .hooks import anonymize_user_data_hook

User = get_user_model()


def delete_data_downloads(user: User, **kwargs):
    for data_download in user.datadownload_set.iterator(chunk_size=50):
        data_download.delete()


def anonymize_user_data(user: User, anonymous_username: str, *, context: dict[str, Any] | None = None):
    anonymize_user_data_hook(
        _anonymize_user_data_action,
        user,
        anonymous_username,
        context = context
    )


def _anonymize_user_data_action(
            user: User,
            anonymous_username: str,
            *,
            context: dict[str, Any] | None = None,
    ):
    """Replaces username with anonymized one, then anonymize their user-specific data
    like username or IP addresses.
    """
    user.username = anonymous_username
    user.slug = slugify(user.username)

    delete_data_downloads(user)

    # update username
    legal_update_usernames(user)
    catetories_update_usernames(user)
    update_actor_name(user)
    anonymize_user_in_thread_events(user)
    anonymize_user_in_likes(user)
    threads_update_usernames(user)
