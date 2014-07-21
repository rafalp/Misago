from misago.conf import settings

from misago.users.avatars import cache, gravatar, dynamic, gallery, uploaded


AVATAR_TYPES = ('gravatar', 'dynamic', 'gallery', 'uploaded')


SET_DEFAULT_AVATAR = {
    'gravatar': gravatar.set_avatar,
    'dynamic': dynamic.set_avatar,
    'gallery': gallery.set_random_avatar
}


def set_default_avatar(user):
    try:
        SET_DEFAULT_AVATAR[settings.default_avatar](user)
    except Exception:
        dynamic.set_avatar(user)


def delete_avatar(user):
    cache.delete_avatar(user)
