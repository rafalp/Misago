from ariadne_graphql_modules import ObjectType, gql


class OffsetPageInfoType(ObjectType):
    __schema__ = gql(
        """
        type OffsetPageInfo {
            number: Int!
            hasNextPage: Boolean!
            hasPreviousPage: Boolean!
            nextPage: Int
            previousPage: Int
            start: Int!
            stop: Int!
        }
        """
    )
    __aliases__ = {
        "hasNextPage": "has_next_page",
        "hasPreviousPage": "has_previous_page",
        "nextPage": "next_page",
        "previousPage": "previous_page",
    }
