from ariadne_graphql_modules import ObjectType, gql


class AvatarType(ObjectType):
    __schema__ = gql(
        """
        type Avatar {
            size: Int!
            url: String!
        }
        """
    )
