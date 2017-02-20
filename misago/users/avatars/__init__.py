from misago.conf import settings

from . import store, gravatar, dynamic, gallery, uploaded

AVATAR_TYPES = ('gravatar', 'dynamic', 'gallery', 'uploaded')

SET_DEFAULT_AVATAR = {
    'gravatar': gravatar.set_avatar,
    'dynamic': dynamic.set_avatar,
    'gallery': gallery.set_random_avatar
}


def set_default_avatar(user, default_avatar, gravatar_fallback):
    try:
        SET_DEFAULT_AVATAR[default_avatar](user)
    except RuntimeError:
        if gallery.galleries_exist():
            SET_DEFAULT_AVATAR[gravatar_fallback](user)
        else:
            dynamic.set_avatar(user)


delete_avatar = store.delete_avatar
