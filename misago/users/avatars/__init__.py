from . import store, gravatar, downloaded, dynamic, gallery, uploaded
from .default import set_default_avatar, set_default_avatar_from_url

__all__ = [
    "AVATAR_TYPES",
    "delete_avatar",
    "downloaded",
    "dynamic",
    "gallery",
    "gravatar",
    "set_default_avatar",
    "set_default_avatar_from_url",
    "store",
    "uploaded",
]

AVATAR_TYPES = ("gravatar", "dynamic", "gallery", "uploaded")

delete_avatar = store.delete_avatar
