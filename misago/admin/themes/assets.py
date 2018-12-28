import hashlib
import io

from PIL import Image
from django.core.files.images import ImageFile

IMAGE_THUMBNAIL_SIZE = (32, 32)


def create_css(theme, css):
    if css_exists(theme, css):
        delete_css(theme, css)
    save_css(theme, css)


def css_exists(theme, css):
    return theme.css.filter(name=css.name).exists()


def delete_css(theme, css):
    theme.css.get(name=css.name).delete()


def save_css(theme, css):
    theme.css.create(
        name=css.name,
        file=css,
        hash=get_file_hash(css),
        size=css.size,
    )


def create_image(theme, image):
    if image_exists(theme, image):
        delete_image(theme, image)
    save_image(theme, image)


def image_exists(theme, image):
    return theme.images.filter(name=image.name).exists()


def delete_image(theme, image):
    theme.images.get(name=image.name).delete()


def save_image(theme, image):
    theme.images.create(
        name=image.name,
        file=image,
        hash=get_file_hash(image),
        type=image.content_type,
        size=image.size,
        thumbnail=get_image_thumbnail(image),
    )


def get_image_thumbnail(image):
    img = Image.open(image.file)
    img.thumbnail(IMAGE_THUMBNAIL_SIZE)
    file = io.BytesIO()
    img.save(file, format="png")
    img.close()

    filename = image.name.split('.')[0]
    return ImageFile(file, name='thumb_%s.png' % filename)


def get_file_hash(file):
    if file.size is None:
        return "00000000"
    file_hash = hashlib.md5()
    for chunk in file.chunks():
        file_hash.update(chunk)
    return file_hash.hexdigest()[:8]