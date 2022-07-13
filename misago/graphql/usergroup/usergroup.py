from ariadne_graphql_modules import ObjectType, gql


class UserGroupType(ObjectType):
    __schema__ = gql(
        """
        type UserGroup {
            id: ID!
            name: String!
            slug: String!
        }
        """
    )


class AdminUserGroupType(ObjectType):
    __schema__ = gql(
        """
        extend type UserGroup {
            isDefault: Boolean!
            isGuest: Boolean!
            isHidden: Boolean!
            isModerator: Boolean!
            isAdmin: Boolean!
        }
        """
    )
    __aliases__ = {
        "isDefault": "is_default",
        "isGuest": "is_guest",
        "isHidden": "is_hidden",
        "isModerator": "is_moderator",
        "isAdmin": "is_admin",
    }
    __requires__ = [UserGroupType]
