import os

from path import path
from PIL import Image

from misago.conf import settings

from misago.users.avatars.paths import AVATARS_STORE


def store_avatar(user, image):
    avatar_dir = get_existing_avatars_dir(user)

    for size in sorted(settings.MISAGO_AVATARS_SIZES, reverse=True):
        image = image.resize((size, size), Image.ANTIALIAS)
        image.save('%s/%s_%s.png' % (avatar_dir, user.pk, size), "PNG")


def delete_avatar(user):
    avatar_dir = get_existing_avatars_dir(user)
    suffixes_to_delete = settings.MISAGO_AVATARS_SIZES + ('org', 'tmp')

    for size in suffixes_to_delete:
        avatar_file = path('%s/%s_%s.png' % (avatar_dir, user.pk, size))
        if avatar_file.exists():
            avatar_file.remove()


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
