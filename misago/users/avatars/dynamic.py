import math
import os
from importlib import import_module

from PIL import Image, ImageColor, ImageDraw, ImageFilter, ImageFont

from misago.conf import settings

from . import store


def set_avatar(user):
    name_bits = settings.MISAGO_DYNAMIC_AVATAR_DRAWER.split('.')

    drawer_module = '.'.join(name_bits[:-1])
    drawer_module = import_module(drawer_module)
    drawer_function = getattr(drawer_module, name_bits[-1])

    image = drawer_function(user)
    store.store_new_avatar(user, image)


"""
Default drawer
"""
def draw_default(user):
    image_size = max(settings.MISAGO_AVATARS_SIZES)

    image = Image.new("RGBA", (image_size, image_size), 0)
    image = draw_avatar_bg(user, image)
    image = draw_avatar_flavour(user, image)

    return image


COLOR_WHEEL = ('#d32f2f', '#c2185b', '#7b1fa2', '#512da8',
               '#303f9f', '#1976d2', '#0288D1', '#0288d1',
               '#0097a7', '#00796b', '#388e3c', '#689f38',
               '#afb42b', '#fbc02d', '#ffa000', '#f57c00',
               '#e64a19')
COLOR_WHEEL_LEN = len(COLOR_WHEEL)


def draw_avatar_bg(user, image):
    image_size = image.size

    color_index = user.pk - COLOR_WHEEL_LEN * (user.pk // COLOR_WHEEL_LEN)
    main_color = COLOR_WHEEL[color_index]

    rgb = ImageColor.getrgb(main_color)

    bg_drawer = ImageDraw.Draw(image)
    bg_drawer.rectangle([(0, 0), image_size], rgb)

    return image


FONT_FILE = os.path.join(os.path.dirname(__file__), 'font.ttf')


def draw_avatar_flavour(user, image):
    string = user.username[0]

    image_size = image.size[0]

    size = int(image_size * 0.7)
    font = ImageFont.truetype(FONT_FILE, size=size)

    text_size = font.getsize(string)
    text_pos = ((image_size - text_size[0]) / 2,
                (image_size - text_size[1]) / 2)

    writer = ImageDraw.Draw(image)
    writer.text(text_pos, string, font=font)

    return image


"""
Some utils for drawring avatar programmatically
"""
CHARS = 'qwertyuiopasdfghjklzxcvbnm1234567890'


def string_to_int(string):
    value = 0
    for p, c in enumerate(string.lower()):
        value += p * (CHARS.find(c))
    return value
