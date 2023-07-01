from django.core.exceptions import ValidationError
from django.utils.translation import pgettext_lazy

from .utils import slugify


class validate_sluggable:
    def __init__(self, error_short=None, error_long=None):
        self.error_short = error_short or pgettext_lazy(
            "sluggable validator", "Value has to contain alpha-numerical characters."
        )
        self.error_long = error_long or pgettext_lazy(
            "sluggable validator", "Value is too long."
        )

    def __call__(self, value):
        slug = slugify(value)

        if not slug.replace("-", ""):
            raise ValidationError(self.error_short)

        if len(slug) > 255:
            raise ValidationError(self.error_long)


def validate_image_square(image):
    if image.width != image.height:
        raise ValidationError(
            pgettext_lazy("image validator", "Uploaded image is not a square.")
        )
