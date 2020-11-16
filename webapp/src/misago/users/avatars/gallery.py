import random
from pathlib import Path

from django.core.files.base import ContentFile
from PIL import Image

from . import store
from ...conf import settings

DEFAULT_GALLERY = "__default__"


def get_available_galleries(include_default=False):
    """
    Returns list of dicts containing 'name' and list of images

    Only jpgs, gifs and pngs are supported avatar images.
    Galleries are
    """
    from ..models import AvatarGallery

    galleries = []
    galleries_dicts = {}

    for image in AvatarGallery.objects.all():
        if image.gallery == DEFAULT_GALLERY and not include_default:
            continue

        if image.gallery not in galleries_dicts:
            galleries_dicts[image.gallery] = {"name": image.gallery, "images": []}

            galleries.append(galleries_dicts[image.gallery])

        galleries_dicts[image.gallery]["images"].append(image)

    return galleries


def galleries_exist():
    from ..models import AvatarGallery

    return AvatarGallery.objects.exists()


def load_avatar_galleries():
    from ..models import AvatarGallery

    galleries = []
    for directory in Path(settings.MISAGO_AVATAR_GALLERY).iterdir():
        if not directory.is_dir():
            continue

        name = directory.name
        images = glob_gallery_images(directory)

        for image in images:
            with open(image, "rb") as image_file:
                galleries.append(
                    AvatarGallery.objects.create(
                        gallery=name, image=ContentFile(image_file.read(), "image")
                    )
                )
    return galleries


def glob_gallery_images(directory):
    images = []
    images.extend(directory.glob("*.gif"))
    images.extend(directory.glob("*.jpg"))
    images.extend(directory.glob("*.jpeg"))
    images.extend(directory.glob("*.png"))
    return images


def set_avatar(user, avatar):
    store.store_new_avatar(user, Image.open(avatar.image))


def set_random_avatar(user):
    galleries = get_available_galleries(include_default=True)
    if not galleries:
        raise RuntimeError("no avatar galleries are set")

    avatars_list = []
    for gallery in galleries:
        if gallery["name"] == DEFAULT_GALLERY:
            avatars_list = gallery["images"]
            break
        else:
            avatars_list += gallery["images"]

    random_avatar = random.choice(avatars_list)
    store.store_new_avatar(user, Image.open(random_avatar.image))
