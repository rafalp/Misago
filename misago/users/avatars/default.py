from . import downloaded, dynamic, gallery, gravatar

SET_DEFAULT_AVATAR = {
    "gravatar": gravatar.set_avatar,
    "dynamic": dynamic.set_avatar,
    "gallery": gallery.set_random_avatar,
}


def set_default_avatar(user, default_avatar, gravatar_fallback):
    try:
        SET_DEFAULT_AVATAR[default_avatar](user)
    except RuntimeError:
        if gallery.galleries_exist():
            SET_DEFAULT_AVATAR[gravatar_fallback](user)
        else:
            dynamic.set_avatar(user)


def set_default_avatar_from_url(user, avatar_url):
    try:
        downloaded.set_avatar(user, avatar_url)
    except RuntimeError:
        dynamic.set_avatar(user)
