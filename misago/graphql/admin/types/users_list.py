from ariadne import ObjectType

users_list_type = ObjectType("UsersList")


@users_list_type.field("page")
async def resolve_users_list_page(obj, *_, page: int = 1):
    return await obj.get_page(page)


@users_list_type.field("pagination")
async def resolve_users_list_pagination(obj, *_):
    await obj.count_pages()
    return obj
