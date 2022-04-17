from ariadne_graphql_modules import ScalarType, gql


class UploadScalar(ScalarType):
    __schema__ = gql("scalar Upload")
