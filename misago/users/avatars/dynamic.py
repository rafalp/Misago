from hashlib import md5
from importlib import import_module
import math
import os

from PIL import Image, ImageDraw, ImageColor, ImageFont, ImageFilter

from misago.conf import settings

from misago.users.avatars import store


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


COLOR_WHEEL = ('#1abc9c', '#2ecc71', '#3498db', '#9b59b6',
               '#f1c40f', '#e67e22', '#e74c3c')
COLOR_WHEEL_LEN = len(COLOR_WHEEL)


def draw_avatar_bg(user, image):
    image_size = image.size

    color_index = user.pk - COLOR_WHEEL_LEN * (user.pk / COLOR_WHEEL_LEN)
    main_color = COLOR_WHEEL[color_index]

    rgb = ImageColor.getrgb(main_color)

    bg_drawer = ImageDraw.Draw(image)
    bg_drawer.rectangle([(0, 0), image_size], rgb)

    image_steps = 4
    step_size = math.ceil(float(image_size[0]) / image_steps)
    for x in xrange(image_steps):
        x_step = float(x + 2) / image_steps

        for y in xrange(image_steps):
            y_step = float(y + 2) / image_steps

            bit_rgb = (int(c * (1 - (x_step * y_step) / 5)) for c in rgb)
            bit_pos = (x * step_size, y * step_size)
            bit_size = (x * step_size + step_size, y * step_size + step_size)
            bg_drawer.rectangle([bit_pos, bit_size], tuple(bit_rgb))

    image = image.filter(ImageFilter.SHARPEN)

    return image


FONT_FILE = os.path.join(os.path.dirname(__file__), 'font.ttf')


def draw_avatar_flavour(user, image):
    string = user.username[0]

    image_size = image.size[0]
    max_string_size = image_size * .8

    size = int(max_string_size)
    font = ImageFont.truetype(FONT_FILE, size=size)
    while max(font.getsize(string)) > max_string_size:
        size -= 1
        font = ImageFont.truetype(FONT_FILE, size=size)

    text_size = font.getsize(string)
    text_pos = ((image_size - text_size[0]) / 2,
                (image_size - text_size[1]) / 2)

    text_shadow = Image.new('RGBA', image.size)
    shadow_color = image.getpixel((image_size - 1, image_size - 1))
    shadow_blur = ImageFilter.GaussianBlur(int(image_size / 5))

    writer = ImageDraw.Draw(text_shadow)
    writer.text(text_pos, string, shadow_color, font=font)
    text_shadow = text_shadow.filter(shadow_blur)

    image = Image.alpha_composite(image, text_shadow)

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
