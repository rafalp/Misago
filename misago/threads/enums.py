from enum import IntEnum

from django.utils.translation import pgettext_lazy


class ThreadPinned(IntEnum):
    NONE = 0
    CATEGORY = 1
    EVERYWHERE = 2

    @classmethod
    def get_choices(cls):
        return (
            (
                cls.NONE,
                pgettext_lazy("pin thread choice", "Don't pin thread"),
            ),
            (
                cls.CATEGORY,
                pgettext_lazy("pin thread choice", "Pin thread in category"),
            ),
            (
                cls.EVERYWHERE,
                pgettext_lazy("pin thread choice", "Pin thread everywhere"),
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
