from ariadne_graphql_modules import ObjectType, gql


class ErrorType(ObjectType):
    __schema__ = gql(
        """
        type Error {
            location: String!
            type: String!
            message: String!
        }
        """
    )
    __aliases__ = {
        "location": "loc",
        "message": "msg",
    }
