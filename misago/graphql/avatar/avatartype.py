from ariadne_graphql_modules import EnumType, gql

from ...avatars import AvatarType


class AvatarTypeEnum(EnumType):
    __schema__ = gql(
        """
        enum AvatarType {
            GRAVATAR
            UPLOAD
        }
        """
    )
    __enum__ = AvatarType
