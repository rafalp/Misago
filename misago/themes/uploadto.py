from django.utils.crypto import get_random_string


def generate_theme_dirname():
    return get_random_string(8)


def upload_css_source_to(instance, filename):
    add_hash_to_filename(instance.source_hash, filename)
    return "themes/%s/css/%s" % (instance.theme.dirname, filename)


def upload_css_to(instance, filename):
    add_hash_to_filename(instance.hash, filename)
    return "themes/%s/css/%s" % (instance.theme.dirname, filename)


def upload_font_to(instance, filename):
    add_hash_to_filename(instance.hash, filename)
    return "themes/%s/font/%s" % (instance.theme.dirname, filename)


def upload_image_to(instance, filename):
    add_hash_to_filename(instance.hash, filename)
    return "themes/%s/media/%s" % (instance.theme.dirname, filename)


def upload_image_thumbnail_to(instance, filename):
    return "themes/%s/media/%s" % (instance.theme.dirname, filename)


def add_hash_to_filename(hash, filename):
    if ".%s." % hash in filename:
        return filename
    extension_start = filename.rfind(".")
    return "%s.%s%s" % (filename[:extension_start], hash, filename[extension_start:])
