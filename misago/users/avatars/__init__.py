from misago.conf import settings

from misago.users.avatars import cache, gravatar, user, gallery, uploaded


AVATAR_TYPES = ('gravatar', 'user', 'gallery', 'uploaded')


SET_DEFAULT_AVATAR = {
    'gravatar': gravatar.set_avatar,
    'user': user.set_avatar,
    'gallery': gallery.set_random_avatar
}


def set_default_avatar(user):
    try:
        SET_DEFAULT_AVATAR[settings.default_avatar](user)
    except Exception:
        SET_DEFAULT_AVATAR['user'](user)


def delete_avatar(user):
    cache.delete_avatar(user)
