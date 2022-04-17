from ariadne_graphql_modules import ObjectType


class BaseAdminQueryType(ObjectType):
    __abstract__ = True

    