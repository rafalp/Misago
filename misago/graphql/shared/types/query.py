from ariadne import QueryType
from graphql import GraphQLResolveInfo

from ....types import Settings


query_type = QueryType()


@query_type.field("settings")
def resolve_settings(_, info: GraphQLResolveInfo) -> Settings:
    return info.context["settings"]
