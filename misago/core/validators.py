from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .utils import slugify


class validate_sluggable:
    def __init__(self, error_short=None, error_long=None):
        self.error_short = error_short or _(
            "Value has to contain alpha-numerical characters."
        )
        self.error_long = error_long or _("Value is too long.")

    def __call__(self, value):
        slug = slugify(value)

        if not slug.replace("-", ""):
            raise ValidationError(self.error_short)

        if len(slug) > 255:
            raise ValidationError(self.error_long)


def validate_image_square(image):
    if image.width != image.height:
        raise ValidationError(_("Uploaded image is not a square."))
