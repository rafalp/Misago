import io

from PIL import Image
from django.core.files.images import ImageFile

from ...core.utils import get_file_hash

IMAGE_TYPES = ("image/gif", "image/png", "image/jpeg", "image/bmp", "image/webp")
THUMBNAIL_SIZE = (32, 32)


def create_media(theme, media):
    if media_exists(theme, media):
        delete_media(theme, media)

    if media_is_image(media):
        save_image(theme, media)
    else:
        save_media(theme, media)


def media_exists(theme, media):
    return theme.media.filter(name=media.name).exists()


def delete_media(theme, media):
    theme.media.get(name=media.name).delete()


def media_is_image(image):
    return image.content_type in IMAGE_TYPES


def save_image(theme, image):
    try:
        img = Image.open(image.file)
    except Exception:  # pylint: disable=broad-except
        return
    else:
        width, height = img.size

    theme.media.create(
        name=image.name,
        file=image,
        hash=get_file_hash(image),
        type=image.content_type,
        width=width,
        height=height,
        size=image.size,
        thumbnail=get_image_thumbnail(img, image.name),
    )

    img.close()


def get_image_thumbnail(image, src_name):
    img = image.copy()
    img.thumbnail(THUMBNAIL_SIZE)
    file = io.BytesIO()
    img.save(file, format="png")
    img.close()

    filename = ".".join(src_name.split(".")[:1])
    return ImageFile(file, name="thumb_%s.png" % filename)


def save_media(theme, media):
    theme.media.create(
        name=media.name,
        file=media,
        hash=get_file_hash(media),
        type=media.content_type,
        size=media.size,
    )
