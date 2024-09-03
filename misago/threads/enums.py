from enum import IntEnum, StrEnum

from django.utils.translation import pgettext_lazy


class ThreadWeight(IntEnum):
    NOT_PINNED = 0
    PINNED_IN_CATEGORY = 1
    PINNED_GLOBALLY = 2


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
