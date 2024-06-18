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
    PILLS = "pills"
    DROPDOWN = "dropdown"

    @classmethod
    def get_choices(cls):
        return (
            (
                cls.FULL,
                pgettext_lazy("category children component choice", "Full panel"),
            ),
            (
                cls.PILLS,
                pgettext_lazy("category children component choice", "Pills"),
            ),
            (
                cls.DROPDOWN,
                pgettext_lazy("category children component choice", "Dropdown"),
            ),
        )
