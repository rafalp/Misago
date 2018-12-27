from django.utils.crypto import get_random_string


def generate_theme_dirname():
    return get_random_string(8)


def upload_css_to(instance, filename):
    filename = filename.replace(".", ".%s." % instance.hash, 1)
    return "themes/%s/%s" % (instance.theme.dirname, filename)


def upload_font_to(instance, filename):
    filename = filename.replace(".", ".%s." % instance.hash, 1)
    return "themes/%s/font/%s" % (instance.theme.dirname, filename)


def upload_image_to(instance, filename):
    filename = filename.replace(".", ".%s." % instance.hash, 1)
    return "themes/%s/img/%s" % (instance.theme.dirname, filename)


def upload_image_thumbnail_to(instance, filename):
    return "themes/%s/img/%s" % (instance.theme.dirname, filename)