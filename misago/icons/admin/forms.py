from io import BytesIO


from PIL import Image
from django import forms
from django.core.files.base import ContentFile
from django.utils.translation import gettext_lazy as _

from ...core.utils import get_file_hash
from ..models import Icon


class IconsForm(forms.Form):
    favicon = forms.ImageField(
        label=_("Upload image"),
        help_text=_(
            "Favicon is small icon that internet browsers display next to your site in "
            "its interface. Uploaded image should be a square that is 48px wide and "
            "tall."
        ),
        required=False,
    )
    apple_touch_icon = forms.ImageField(
        label=_("Upload image"),
        help_text=_(
            "Apple devices and Safari web browser will use this image to represent the "
            "site in its interfaces. Uploaded image should be square at least 180px "
            "wide and tall."
        ),
        required=False,
    )

    def save(self):
        if self.cleaned_data.get("favicon"):
            self.save_favicon(self.cleaned_data["favicon"])
        if self.cleaned_data.get("apple_touch_icon"):
            self.save_apple_touch_icon(self.cleaned_data["apple_touch_icon"])

    def save_favicon(self, image):
        for icon in Icon.objects.filter(type__in=Icon.TYPE_FAVICON):
            icon.image.delete(save=False)
            icon.delete()

        save_favicon(image)
        save_icon(image, (32, 32), "favicon_32")
        save_icon(image, (16, 16), "favicon_16")

    def save_apple_touch_icon(self, image):
        for icon in Icon.objects.filter(type=Icon.TYPE_APPLE_TOUCH_ICON):
            icon.image.delete(save=False)
            icon.delete()

        save_icon(image, (180, 180), Icon.TYPE_APPLE_TOUCH_ICON)


def save_favicon(image):
    icon = Image.open(image)

    buffer = BytesIO()
    icon.save(buffer, "ICO", sizes=((16, 16), (32, 32), (48, 48)))
    buffer.seek(0)

    icon_file = ContentFile(buffer.read())
    icon_file.name = "{}.{}.ico".format("favicon", get_file_hash(icon_file))

    Icon.objects.create(type="favicon", image=icon_file)


def save_icon(image, size, icon_type):
    icon = Image.open(image)
    icon.thumbnail(size)

    buffer = BytesIO()
    icon.save(buffer, "PNG")
    buffer.seek(0)

    icon_file = ContentFile(buffer.read())
    icon_file.name = "{}.{}.png".format(
        icon_type.replace("_", "-"), get_file_hash(icon_file)
    )

    Icon.objects.create(
        type=icon_type,
        image=icon_file,
        width=size[0],
        height=size[1],
    )