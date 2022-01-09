from hashlib import md5
from typing import Any, Dict, Iterable, Optional

from ariadne import ObjectType

from ....avatars.types import AvatarType
from ....conf import settings
from ....uploads.urls import make_media_url
from ....users.models import User

user_type = ObjectType("User")

user_type.set_alias("fullName", "full_name")
user_type.set_alias("joinedAt", "joined_at")
user_type.set_alias("isModerator", "is_moderator")
user_type.set_alias("isAdmin", "is_admin")


@user_type.field("avatars")
def resolve_avatars(user: User, _) -> Iterable[Dict[str, Any]]:
    if user.avatar_type == AvatarType.UPLOAD and user.avatars:
        for avatar in user.avatars:
            yield {
                "size": avatar["size"],
                "url": make_media_url(avatar["image"]),
            }
        return

    avatar_hash = md5(user.email.encode("utf-8")).hexdigest()
    for size in settings.avatar_sizes:
        yield {
            "size": size,
            "url": f"https://www.gravatar.com/avatar/{avatar_hash}?s={size}&d=identicon",
        }


@user_type.field("avatar")
def resolve_avatar(user: User, _, size: Optional[int] = None) -> Dict[str, Any]:
    if user.avatar_type == AvatarType.UPLOAD and user.avatars:
        if size:
            for avatar in reversed(user.avatars):
                if avatar["size"] > size:
                    return avatar

        return user.avatars[0]

    avatar_hash = md5(user.email.encode("utf-8")).hexdigest()
    resolved_size = size or max(settings.avatar_sizes)

    return {
        "size": resolved_size,
        "url": f"https://www.gravatar.com/avatar/{avatar_hash}?s={resolved_size}&d=identicon",
    }
