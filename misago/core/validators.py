import re

from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
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


validate_color_hex = RegexValidator(
    re.compile(r"^#[0-9a-f][0-9a-f][0-9a-f]([0-9a-f][0-9a-f][0-9a-f]?)$", re.I),
    pgettext_lazy(
        "color hex validator",
        "Entered value is not a valid color in the hex format (eg. #FA8072).",
    ),
    "invalid",
)


validate_css_name = RegexValidator(
    re.compile(r"^[a-zA-Z_-]+([a-zA-Z0-9-_]+)?$"),
    pgettext_lazy(
        "css name validator",
        "Enter a valid CSS class name that starts with a Latin letter, underscore, or a hyphen, and is followed by any combination of Latin letters, numbers, hyphens, and underscore characters.",
    ),
    "invalid",
)
