from io import BytesIO


from PIL import Image
from django import forms
from django.core.files.base import ContentFile
from django.utils.translation import gettext_lazy as _

from ...core.utils import get_file_hash
from ...core.validators import validate_image_square
from ..models import Icon

FAVICON_MIN_SIZE = 48
FAVICON_SIZES = ((16, 16), (32, 32), (48, 48))
APPLE_TOUCH_MIN_SIZE = 180
VALID_MIME = ("image/gif", "image/jpeg", "image/png")


class IconsForm(forms.Form):
    favicon = forms.ImageField(
        label=_("Upload image"),
        help_text=_("Uploaded image should be a square that is 48px wide and tall."),
        required=False,
    )
    favicon_delete = forms.BooleanField(label=_("Delete custom icon"), required=False)

    apple_touch_icon = forms.ImageField(
        label=_("Upload image"),
        help_text=_("Uploaded image should be square at least 180px wide and tall."),
        required=False,
    )
    apple_touch_icon_delete = forms.BooleanField(
        label=_("Delete custom icon"), required=False
    )

    def clean_favicon(self):
        upload = self.cleaned_data.get("favicon")
        if not upload or upload == self.initial.get("favicon"):
            return None

        validate_image_square(upload.image)
        validate_image_dimensions(upload.image, FAVICON_MIN_SIZE)
        validate_image_mime_type(upload)

        return upload

    def clean_apple_touch_icon(self):
        upload = self.cleaned_data.get("apple_touch_icon")
        if not upload or upload == self.initial.get("apple_touch_icon"):
            return None

        validate_image_square(upload.image)
        validate_image_dimensions(upload.image, APPLE_TOUCH_MIN_SIZE)
        validate_image_mime_type(upload)

        return upload

    def save(self):
        if self.cleaned_data.get("favicon"):
            self.save_favicon(self.cleaned_data["favicon"])
        elif self.cleaned_data.get("favicon_delete"):
            self.delete_icons(Icon.FAVICON_TYPES)

        if self.cleaned_data.get("apple_touch_icon"):
            self.save_apple_touch_icon(self.cleaned_data["apple_touch_icon"])
        elif self.cleaned_data.get("apple_touch_icon_delete"):
            self.delete_icons([Icon.TYPE_APPLE_TOUCH_ICON])

    def save_favicon(self, image):
        self.delete_icons(Icon.FAVICON_TYPES)
        save_favicon(image)
        save_icon(image, (32, 32), Icon.TYPE_FAVICON_32)
        save_icon(image, (16, 16), Icon.TYPE_FAVICON_16)

    def save_apple_touch_icon(self, image):
        self.delete_icons([Icon.TYPE_APPLE_TOUCH_ICON])
        save_icon(image, (180, 180), Icon.TYPE_APPLE_TOUCH_ICON)

    def delete_icons(self, icon_types):
        for icon in Icon.objects.filter(type__in=icon_types):
            icon.delete()


def save_favicon(image):
    icon = Image.open(image)

    buffer = BytesIO()
    icon.save(buffer, "ICO", sizes=FAVICON_SIZES)
    buffer.seek(0)

    icon_file = ContentFile(buffer.read())
    icon_file.name = "%s.%s.ico" % ("favicon", get_file_hash(icon_file))

    Icon.objects.create(type=Icon.TYPE_FAVICON, image=icon_file, size=icon_file.size)


def save_icon(image, size, icon_type):
    icon = Image.open(image)
    icon.thumbnail(size)

    buffer = BytesIO()
    icon.save(buffer, "PNG")
    buffer.seek(0)

    icon_file = ContentFile(buffer.read())
    icon_file.name = "%s.%s.png" % (
        icon_type.replace("_", "-"),
        get_file_hash(icon_file),
    )

    Icon.objects.create(type=icon_type, image=icon_file, size=icon_file.size)


def validate_image_dimensions(image, size):
    if image.width < size:
        raise forms.ValidationError(
            _("Uploaded image's edge should be at least %(size)s pixels long.")
            % {"size": size}
        )


def validate_image_mime_type(upload):
    if upload.content_type not in VALID_MIME:
        raise forms.ValidationError(_("Uploaded image was not gif, jpeg or png."))
