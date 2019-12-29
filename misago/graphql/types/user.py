from hashlib import md5
from typing import Any, Dict, Iterable

from ariadne import ObjectType

from ...conf import settings
from ...types import User


user_type = ObjectType("User")

user_type.set_alias("joinedAt", "joined_at")
user_type.set_alias("isModerator", "is_moderator")
user_type.set_alias("isAdministrator", "is_administrator")


@user_type.field("avatars")
def resolve_avatars(user: User, _) -> Iterable[Dict[str, Any]]:
    avatar_hash = md5(user.email.encode("utf-8")).hexdigest()
    for size in settings.avatar_sizes:
        yield {
            "size": size,
            "url": f"https://www.gravatar.com/avatar/{avatar_hash}?s={size}&d=identicon",
        }
