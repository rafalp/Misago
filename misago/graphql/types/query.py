from ariadne import QueryType


query_type = QueryType()


@query_type.field("settings")
def resolve_settings(_, info):
    return info.context["settings"]
