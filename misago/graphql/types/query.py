from ariadne import QueryType

from ...auth import get_authenticated_user


query_type = QueryType()


@query_type.field("auth")
async def resolve_auth(_, info):
    return await get_authenticated_user(info.context)


@query_type.field("settings")
def resolve_settings(_, info):
    return info.context["settings"]
