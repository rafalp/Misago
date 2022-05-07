from ariadne_graphql_modules import ObjectType, gql


class ForumStatsType(ObjectType):
    __schema__ = gql(
        """
        type ForumStats {
            id: ID!
            threads: Int!
            posts: Int!
            users: Int!
        }
        """
    )
