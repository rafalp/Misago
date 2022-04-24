from ariadne_graphql_modules import ObjectType, gql


class PageInfoType(ObjectType):
    __schema__ = gql(
        """
        type PageInfo {
            hasNextPage: Boolean!
            hasPreviousPage: Boolean!
            startCursor: String
            endCursor: String
            nextCursor: String
            previousCursor: String
        }
        """
    )
    __aliases__ = {
        "hasNextPage": "has_next_page",
        "hasPreviousPage": "has_previous_page",
        "startCursor": "start_cursor",
        "endCursor": "end_cursor",
        "nextCursor": "next_cursor",
        "previousCursor": "previous_cursor",
    }
