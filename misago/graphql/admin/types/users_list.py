from ariadne import ObjectType

from ....database.paginator import PageDoesNotExist
from ...cache import cached_resolver

users_list_type = ObjectType("UsersList")


@users_list_type.field("page")
@cached_resolver
async def resolve_users_list_page(obj, *_, page: int = 1):
    try:
        return await obj.get_page(page)
    except PageDoesNotExist:
        return None


@users_list_type.field("pagination")
async def resolve_users_list_pagination(obj, *_):
    return obj
