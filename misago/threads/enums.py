from enum import IntEnum

from django.utils.translation import pgettext_lazy


class ThreadWeight(IntEnum):
    NOT_PINNED = 0
    PINNED_IN_CATEGORY = 1
    PINNED_GLOBALLY = 2

    @classmethod
    def get_choices(cls):
        return (
            (
                cls.NOT_PINNED,
                pgettext_lazy("pin thread choice", "Don't pin thread"),
            ),
            (
                cls.PINNED_IN_CATEGORY,
                pgettext_lazy("pin thread choice", "Pin thread in category"),
            ),
            (
                cls.PINNED_GLOBALLY,
                pgettext_lazy("pin thread choice", "Pin thread globally"),
            ),
        )


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
