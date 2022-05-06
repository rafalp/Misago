from ariadne_graphql_modules import ScalarType, gql


class RichTextScalar(ScalarType):
    __schema__ = gql(
        """
        scalar RichText
        """
    )
