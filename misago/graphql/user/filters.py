from ariadne_graphql_modules import InputType, gql


class AdminUserFilters(InputType):
    __schema__ = gql(
        """
        input UserFilters {
            name: String
            email: String
            isActive: Boolean
            isModerator: Boolean
            isAdmin: Boolean
        }
        """
    )
    __args__ = {
        "isActive": "is_active",
        "isModerator": "is_moderator",
        "isAdmin": "is_admin",
    }
