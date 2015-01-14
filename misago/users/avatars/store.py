from hashlib import md5
import os

from path import Path
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
        avatar_file = '%s_%s.png' % (user.pk, size)
        avatar_file = Path(os.path.join(avatars_dir, avatar_file))

        image = image.resize((size, size), Image.ANTIALIAS)
        image.save(avatar_file, "PNG")


def delete_avatar(user):
    avatars_dir = get_existing_avatars_dir(user)
    suffixes_to_delete = settings.MISAGO_AVATARS_SIZES + ('org', 'tmp')

    for size in suffixes_to_delete:
        avatar_file = '%s_%s.png' % (user.pk, size)
        avatar_file = Path(os.path.join(avatars_dir, avatar_file))
        if avatar_file.exists():
            avatar_file.remove()


def store_temporary_avatar(user, image):
    avatars_dir = get_existing_avatars_dir(user)
    avatar_file = '%s_tmp.png' % user.pk

    normalize_image(image)
    image.save(os.path.join(avatars_dir, avatar_file), "PNG")


def store_original_avatar(user):
    org_path = avatar_file_path(user, 'org')
    if org_path.exists():
        org_path.remove()
    avatar_file_path(user, 'tmp').rename(org_path)


def avatar_file_path(user, size):
    avatars_dir = get_existing_avatars_dir(user)
    avatar_file = '%s_%s.png' % (user.pk, size)
    return Path(os.path.join(avatars_dir, avatar_file))


def avatar_file_exists(user, size):
    return avatar_file_path(user, size).exists()


def store_new_avatar(user, image):
    """
    Deletes old image before storing new one
    """
    delete_avatar(user)
    store_avatar(user, image)


def get_avatars_dir_path(user=None):
    if user:
        try:
            user_id = user.pk
        except AttributeError:
            user_id = user

        dir_hash = md5(str(user_id)).hexdigest()
        hash_path = [dir_hash[0:1], dir_hash[2:3]]
        return Path(os.path.join(AVATARS_STORE, *hash_path))
    else:
        return Path(os.path.join(AVATARS_STORE, 'blank'))


def get_existing_avatars_dir(user=None):
    avatars_dir = get_avatars_dir_path(user)
    if not avatars_dir.exists():
        avatars_dir.makedirs()
    return avatars_dir
