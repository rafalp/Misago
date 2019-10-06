from ariadne import QueryType


query_type = QueryType()


@query_type.field("settings")
def resolve_settings(*_):
    return {"forum_name": "Misago"}
