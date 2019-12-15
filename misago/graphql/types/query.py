from ariadne import QueryType

from ...auth import get_authenticated_user
from ...loaders import load_categories, load_category


query_type = QueryType()


@query_type.field("auth")
async def resolve_auth(_, info):
    return await get_authenticated_user(info.context)


@query_type.field("categories")
async def resolve_categories(_, info):
    return await load_categories(info.context)


@query_type.field("category")
async def resolve_category(_, info, *, id):  # pylint: disable=redefined-builtin
    return await load_category(info.context, id)


@query_type.field("settings")
def resolve_settings(_, info):
    return info.context["settings"]
