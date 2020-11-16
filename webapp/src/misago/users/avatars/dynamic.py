import os

from django.utils.module_loading import import_string
from PIL import Image, ImageColor, ImageDraw, ImageFont

from . import store
from ...conf import settings

COLOR_WHEEL = (
    "#d32f2f",
    "#c2185b",
    "#7b1fa2",
    "#512da8",
    "#303f9f",
    "#1976d2",
    "#0288D1",
    "#0288d1",
    "#0097a7",
    "#00796b",
    "#388e3c",
    "#689f38",
    "#afb42b",
    "#fbc02d",
    "#ffa000",
    "#f57c00",
    "#e64a19",
)
COLOR_WHEEL_LEN = len(COLOR_WHEEL)
FONT_FILE = os.path.join(os.path.dirname(__file__), "font.ttf")


def set_avatar(user):
    drawer_function = import_string(settings.MISAGO_DYNAMIC_AVATAR_DRAWER)

    image = drawer_function(user)
    store.store_new_avatar(user, image)


def draw_default(user):
    """default avatar drawer that draws username's first letter on color"""
    image_size = max(settings.MISAGO_AVATARS_SIZES)

    image = Image.new("RGBA", (image_size, image_size), 0)
    image = draw_avatar_bg(user, image)
    image = draw_avatar_flavour(user, image)

    return image


def draw_avatar_bg(user, image):
    image_size = image.size

    color_index = user.pk - COLOR_WHEEL_LEN * (user.pk // COLOR_WHEEL_LEN)
    main_color = COLOR_WHEEL[color_index]

    rgb = ImageColor.getrgb(main_color)

    bg_drawer = ImageDraw.Draw(image)
    bg_drawer.rectangle([(0, 0), image_size], rgb)

    return image


def draw_avatar_flavour(user, image):
    string = user.username[0]

    image_size = image.size[0]

    size = int(image_size * 0.7)
    font = ImageFont.truetype(FONT_FILE, size=size)

    text_size = font.getsize(string)
    text_pos = ((image_size - text_size[0]) / 2, (image_size - text_size[1]) / 2)

    writer = ImageDraw.Draw(image)
    writer.text(text_pos, string, font=font)

    return image
