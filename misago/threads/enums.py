from enum import IntEnum, StrEnum

from django.utils.translation import pgettext_lazy


class ThreadWeight(IntEnum):
    NOT_PINNED = 0
    PINNED_IN_CATEGORY = 1
    PINNED_GLOBALLY = 2


class ThreadsUrls(StrEnum):
    thread = "misago:thread"
    post = "misago:thread-post"
    new_post = "misago:thread-new"
    last_post = "misago:thread-last"
    unapproved_post = "misago:thread-unapproved"
    best_answer = "misago:thread-best-answer"


class PrivateThreadsUrls(StrEnum):
    thread = "misago:private-thread"
    post = "misago:private-thread-post"
    new_post = "misago:private-thread-new"
    last_post = "misago:private-thread-last"
    unapproved_post = "misago:private-thread-unapproved"
    best_answer = "misago:private-thread-best-answer"


class ThreadsListsPolling(IntEnum):
    DISABLED = 0
    ENABLED_FOR_USERS = 1
    ENABLED = 2

    @classmethod
    def get_choices(cls):
        return (
            (
                cls.ENABLED,
                pgettext_lazy(
                    "threads lists polling choice",
                    "Enable for both signed-in users and guests",
                ),
            ),
            (
                cls.ENABLED_FOR_USERS,
                pgettext_lazy(
                    "category lists polling choice", "Enable for signed-in users"
                ),
            ),
            (
                cls.DISABLED,
                pgettext_lazy("category lists polling choice", "Disable"),
            ),
        )
