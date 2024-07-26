from enum import IntEnum, StrEnum

from django.utils.translation import pgettext_lazy


class CategoryTree(IntEnum):
    THREADS = 0
    PRIVATE_THREADS = 1


class CategoryTreeDeprecated(IntEnum):
    PRIVATE_THREADS = 0
    THREADS = 1


class CategoryChildrenComponent(StrEnum):
    FULL = "full"
    DROPDOWN = "dropdown"
    DISABLED = "disabled"

    @classmethod
    def get_category_choices(cls):
        return (
            (
                cls.FULL,
                pgettext_lazy("category children component choice", "Full panel"),
            ),
            (
                cls.DROPDOWN,
                pgettext_lazy("category children component choice", "Dropdown"),
            ),
        )

    @classmethod
    def get_threads_choices(cls):
        return (
            (
                cls.DISABLED,
                pgettext_lazy("category children component choice", "Disabled"),
            ),
        ) + cls.get_category_choices()
