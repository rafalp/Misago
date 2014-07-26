import os

from path import path
from PIL import Image

from misago.conf import settings

from misago.users.avatars.paths import AVATARS_STORE


def normalize_image(image):
    """if image is gif, strip it of animation"""
    image.seek(0)
    return image.copy().convert('RGBA')


def store_avatar(user, image):
    avatars_dir = get_existing_avatars_dir(user)

    normalize_image(image)
    for size in sorted(settings.MISAGO_AVATARS_SIZES, reverse=True):
        image = image.resize((size, size), Image.ANTIALIAS)
        image.save('%s/%s_%s.png' % (avatars_dir, user.pk, size), "PNG")


def delete_avatar(user):
    avatars_dir = get_existing_avatars_dir(user)
    suffixes_to_delete = settings.MISAGO_AVATARS_SIZES + ('org', 'tmp')

    for size in suffixes_to_delete:
        avatar_file = path('%s/%s_%s.png' % (avatars_dir, user.pk, size))
        if avatar_file.exists():
            avatar_file.remove()


def store_temporary_avatar(user, image):
    avatars_dir = get_existing_avatars_dir(user)
    normalize_image(image)
    image.save('%s/%s_tmp.png' % (avatars_dir, user.pk), "PNG")


def store_original_avatar(user):
    org_path = avatar_file_path(user, 'org')
    if org_path.exists():
        org_path.remove()
    avatar_file_path(user, 'tmp').rename(org_path)


def avatar_file_path(user, size):
    avatars_dir = get_existing_avatars_dir(user)
    return path('%s/%s_%s.png' % (avatars_dir, user.pk, size))


def avatar_file_exists(user, size):
    return avatar_file_path(user, size).exists()


def store_new_avatar(user, image):
    """
    Deletes old image before storing new one
    """
    delete_avatar(user)
    store_avatar(user, image)


def get_existing_avatars_dir(user):
    date_dir = unicode(user.joined_on.strftime('%y%m'))
    avatars_dir = path(os.path.join(AVATARS_STORE, date_dir))

    if not avatars_dir.exists():
        avatars_dir.mkdir()
    return avatars_dir
