from misago.conf import settings

from misago.users.avatars import store, gravatar, dynamic, gallery, uploaded


AVATAR_TYPES = ('gravatar', 'dynamic', 'gallery', 'uploaded')


SET_DEFAULT_AVATAR = {
    'gravatar': gravatar.set_avatar,
    'dynamic': dynamic.set_avatar,
    'gallery': gallery.set_random_avatar
}


def set_default_avatar(user):
    try:
        SET_DEFAULT_AVATAR[settings.default_avatar](user)
    except RuntimeError:
        if gallery.galleries_exist():
            SET_DEFAULT_AVATAR[settings.default_gravatar_fallback](user)
        else:
            dynamic.set_avatar(user)


get_avatar_hash = store.get_avatar_hash
delete_avatar = store.delete_avatar
