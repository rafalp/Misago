from enum import IntEnum, StrEnum

from django.utils.translation import pgettext_lazy


class ThreadWeight(IntEnum):
    NOT_PINNED = 0
    PINNED_IN_CATEGORY = 1
    PINNED_GLOBALLY = 2


class ThreadUrl(StrEnum):
    THREAD = "misago:thread"
    POST = "misago:thread-post"
    NEW_POST = "misago:thread-new"
    LAST_POST = "misago:thread-last"
    UNAPPROVED_POST = "misago:thread-unapproved"
    BEST_ANSWER = "misago:thread-best-answer"


class PrivateThreadUrl(StrEnum):
    THREAD = "misago:private-thread"
    POST = "misago:private-thread-post"
    NEW_POST = "misago:private-thread-new"
    LAST_POST = "misago:private-thread-last"
    UNAPPROVED_POST = "misago:private-thread-unapproved"
    BEST_ANSWER = "misago:private-thread-best-answer"


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
