import os
from hashlib import md5

from django.utils.encoding import force_bytes

from path import Path
from PIL import Image

from misago.conf import settings

from .paths import AVATARS_STORE


def normalize_image(image):
    """if image is gif, strip it of animation"""
    image.seek(0)
    return image.copy().convert('RGBA')


def get_avatar_hash(user, suffix=None):
    avatars_dir = get_existing_avatars_dir(user)

    avatar_suffix = suffix or max(settings.MISAGO_AVATARS_SIZES)
    avatar_file = '%s_%s.png' % (user.pk, avatar_suffix)
    avatar_file = Path(os.path.join(avatars_dir, avatar_file))

    md5_hash = md5()

    with open(avatar_file, 'rb') as f:
        while True:
            data = f.read(128)
            if not data:
                break
            md5_hash.update(data)
    return md5_hash.hexdigest()[:8]


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


def get_user_avatar_tokens(user):
    token_seeds = (user.email, user.avatar_hash, settings.SECRET_KEY)

    tokens = {
        'org': md5(force_bytes('org:%s:%s:%s' % token_seeds)).hexdigest()[:8],
        'tmp': md5(force_bytes('tmp:%s:%s:%s' % token_seeds)).hexdigest()[:8],
    }

    tokens.update({
        tokens['org']: 'org',
        tokens['tmp']: 'tmp',
    })

    return tokens


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
            user_pk = user.pk
        except AttributeError:
            user_pk = user

        dir_hash = md5(str(user_pk).encode()).hexdigest()
        hash_path = [dir_hash[0:1], dir_hash[2:3]]
        return Path(os.path.join(AVATARS_STORE, *hash_path))
    else:
        return Path(os.path.join(AVATARS_STORE, 'blank'))


def get_existing_avatars_dir(user=None):
    avatars_dir = get_avatars_dir_path(user)
    if not avatars_dir.exists():
        avatars_dir.makedirs()
    return avatars_dir
