from django.utils.crypto import get_random_string


def generate_theme_dirname():
    return get_random_string(8)


def upload_source_css_to(instance, filename):
    filename = add_hash_to_filename(instance.source_hash, filename)
    return "themes/%s/css/%s" % (instance.theme.dirname, filename)


def upload_build_css_to(instance, filename):
    filename = add_hash_to_filename(instance.build_hash, filename)
    return "themes/%s/css/%s" % (instance.theme.dirname, filename)


def upload_media_to(instance, filename):
    filename = add_hash_to_filename(instance.hash, filename)
    return "themes/%s/media/%s" % (instance.theme.dirname, filename)


def upload_media_thumbnail_to(instance, filename):
    return "themes/%s/media/%s" % (instance.theme.dirname, filename)


def add_hash_to_filename(hash, filename):  # pylint: disable=redefined-builtin
    if ".%s." % hash in filename:
        return filename
    extension_start = filename.rfind(".")
    return "%s.%s%s" % (filename[:extension_start], hash, filename[extension_start:])
