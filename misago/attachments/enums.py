from enum import StrEnum

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
