from enum import StrEnum

from django.utils.translation import pgettext_lazy


class CategoryPermission(StrEnum):
    SEE = pgettext_lazy("category permission", "See category")
    READ = pgettext_lazy("category permission", "Read threads")
    START = pgettext_lazy("category permission", "Start threads")
    REPLY = pgettext_lazy("category permission", "Reply threads")
    ATTACHMENTS = pgettext_lazy("category permission", "Attachments")
