from ariadne_graphql_modules import EnumType, gql


class AdminUserSortByEnum(EnumType):
    __schema__ = gql(
        """
        enum UserSortBy {
            JOINED_FIRST
            JOINED_LAST
            NAME_ASC
            NAME_DESC
        }
        """
    )
    __enum__ = {
        "JOINED_FIRST": "id",
        "JOINED_LAST": "-id",
        "NAME_ASC": "slug",
        "NAME_DESC": "-slug",
    }
