import random

from path import Path
from PIL import Image

from django.conf import settings

from misago.users.avatars import store
from misago.users.avatars.paths import MEDIA_AVATARS


def get_available_galleries(include_default=False):
    """
    Returns list of dicts containing 'name' and list of images

    Only jpgs, gifs and pngs are supported avatar images.
    Galleries are
    """
    galleries = []

    for directory in Path(MEDIA_AVATARS).dirs():
        if include_default or directory[-8:] != '_default':
            gallery = {'name': directory.name, 'images': []}

            images = directory.files('*.gif')
            images += directory.files('*.jpg')
            images += directory.files('*.jpeg')
            images += directory.files('*.png')

            for image in images:
                image_path = image[len(settings.MEDIA_ROOT):]
                if image_path.startswith('/'):
                    image_path = image_path[1:]
                gallery['images'].append(image_path)

            if gallery['images']:
                galleries.append(gallery)

    return galleries


def galleries_exist():
    return bool(get_available_galleries())


def is_avatar_from_gallery(image_path):
    for gallery in get_available_galleries():
        if image_path in gallery['images']:
            return True
    else:
        return False


def set_avatar(user, gallery_image_path):
    image = Image.open('%s/%s' % (settings.MEDIA_ROOT, gallery_image_path))
    store.store_new_avatar(user, image)


def set_random_avatar(user):
    galleries = get_available_galleries(include_default=True)
    if not galleries:
        raise RuntimeError("no avatar galleries are set")

    avatars_list = []

    for gallery in galleries:
        if gallery['name'] == '_default':
            avatars_list = gallery['images']
            break
        else:
            avatars_list += gallery['images']

    set_avatar(user, random.choice(avatars_list))
