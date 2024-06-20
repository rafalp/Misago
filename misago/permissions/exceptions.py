from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.utils.translation import pgettext


class CategoryNotFoundError(Http404):
    def __str__(self) -> str:
        return pgettext(
            "category permission error",
            "This category doesn't exist or you don't have permission to see it.",
        )


class CategoryBrowseError(PermissionDenied):
    def __str__(self) -> str:
        return pgettext(
            "category permission error",
            "You can't browse the contents of this category.",
        )
