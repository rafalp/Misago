from enum import IntEnum, StrEnum

from django.utils.translation import pgettext_lazy


class AllowedAttachments(StrEnum):
    ALL = "all"
    MEDIA = "media"
    IMAGES = "images"
    NONE = "none"

    @classmethod
    def get_choices(cls):
        return (
            (
                cls.ALL.value,
                pgettext_lazy("allowed attachment type", "All supported types"),
            ),
            (
                cls.MEDIA.value,
                pgettext_lazy("allowed attachment type", "Images and videos"),
            ),
            (cls.IMAGES.value, pgettext_lazy("allowed attachment type", "Images only")),
            (
                cls.NONE.value,
                pgettext_lazy("allowed attachment type", "Disable uploads"),
            ),
        )


class AttachmentType(StrEnum):
    IMAGE = "image"
    VIDEO = "video"
    OTHER = "other"


class AttachmentTypeRestriction(StrEnum):
    REQUIRE = "require"
    DISALLOW = "disallow"

    @classmethod
    def get_choices(cls):
        return (
            (
                cls.REQUIRE.value,
                pgettext_lazy(
                    "attachment type restriction",
                    "Require uploaded files to have extensions from the list",
                ),
            ),
            (
                cls.DISALLOW.value,
                pgettext_lazy(
                    "attachment type restriction",
                    "Disallow uploads of files with listed extensions",
                ),
            ),
        )


class AttachmentStorage(IntEnum):
    GLOBAL = 0
    USER_TOTAL = 1
    USER_UNUSED = 2
