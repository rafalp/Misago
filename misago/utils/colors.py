from colorsys import rgb_to_hsv, hsv_to_rgb

def rgb_to_hex(r, g, b):
    r = unicode(hex(int(r * 255))[2:]).zfill(2)
    g = unicode(hex(int(g * 255))[2:]).zfill(2)
    b = unicode(hex(int(b * 255))[2:]).zfill(2)
    return r + g+ b


def hex_to_rgb(color):
    if len(color) == 6:
        r, g, b = color[0:2], color[2:4], color[4:6]
    elif len(color) == 3:
        r, g, b = color[0], color[1], color[2]
    else:
        raise ValueError('"%s" is not correct HTML Hex Color.')

    r, g, b = float(int(r, 16)), float(int(g, 16)), float(int(b, 16))

    r /= 255.0
    g /= 255.0
    b /= 255.0
    return r, g, b


def spin(color, rad):
    append_hex = False
    if color[0] == '#':
        append_hex = True
        color = color[1:]

    r, g, b = hex_to_rgb(color)
    h, s, v = rgb_to_hsv(r, g, b)
    if rad:
        h += float(rad) / 360

    r, g, b = hsv_to_rgb(h, s, v)

    if append_hex:
        return '#' + rgb_to_hex(r, g, b)
    return rgb_to_hex(r, g, b)


def desaturate(color, steps, step, minimum=0):
    append_hex = False
    if color[0] == '#':
        append_hex = True
        color = color[1:]

    r, g, b = hex_to_rgb(color)
    h, s, v = rgb_to_hsv(r, g, b)

    minimum /= 100.0
    scope = s - minimum
    s = minimum + (scope / steps * (steps - step))

    r, g, b = hsv_to_rgb(h, s, v)

    if append_hex:
        return '#' + rgb_to_hex(r, g, b)
    return rgb_to_hex(r, g, b)


def lighten(color, steps, step, maximum=100):
    append_hex = False
    if color[0] == '#':
        append_hex = True
        color = color[1:]

    r, g, b = hex_to_rgb(color)

    scope = maximum / 100.0 - min(r, g, b)
    step = scope / steps * step

    r += step
    g += step
    b += step

    r = 1 if r > 1 else r
    g = 1 if g > 1 else g
    b = 1 if b > 1 else b

    if append_hex:
        return '#' + rgb_to_hex(r, g, b)
    return rgb_to_hex(r, g, b)


def darken(color, steps, step, minimum=0):
    append_hex = False
    if color[0] == '#':
        append_hex = True
        color = color[1:]

    r, g, b = hex_to_rgb(color)

    scope = minimum / 100.0 - max(r, g, b)
    step = scope / steps * step

    r += step
    g += step
    b += step

    r = 0 if r < 0 else r
    g = 0 if g < 0 else g
    b = 0 if b < 0 else b

    if append_hex:
        return '#' + rgb_to_hex(r, g, b)
    return rgb_to_hex(r, g, b)