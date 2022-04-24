from hashlib import md5
from typing import Any, Dict, Iterable, Optional

from ariadne_graphql_modules import ObjectType, gql

from ...avatars.types import AvatarType
from ...conf import settings
from ...uploads.urls import make_media_url
from ...users.models import User

from ..avatars import AvatarType as AvatarGraphQLType, AvatarTypeEnum
from ..scalars import DateTimeScalar


class UserType(ObjectType):
    __schema__ = gql(
        """
        type User {
            id: ID!
            name: String!
            slug: String!
            email: String!
            fullName: String
            isModerator: Boolean!
            isAdmin: Boolean!
            joinedAt: DateTime!
            avatars: [Avatar!]!
            avatar(size: Int): Avatar!
            avatarType: AvatarType!
        }
        """
    )
    __aliases__ = {
        "fullName": "full_name",
        "isModerator": "is_moderator",
        "isAdmin": "is_admin",
        "joinedAt": "joined_at",
        "avatarType": "avatar_type",
    }
    __requires__ = [AvatarGraphQLType, AvatarTypeEnum, DateTimeScalar]

    @staticmethod
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

    @staticmethod
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


class AdminUserType(ObjectType):
    __schema__ = gql(
        """
        extend type User {
            isActive: Boolean!
        }
        """
    )
    __aliases__ = {"isActive": "is_active"}
    __requires__ = [UserType]
