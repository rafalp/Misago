from typing import Optional, cast

from ariadne import ObjectType
from graphql import GraphQLResolveInfo

from ...loaders import load_category, load_thread, load_user
from ...types import Category, Post, Thread, User


post_type = ObjectType("Post")

post_type.set_alias("posterName", "poster_name")
post_type.set_alias("postedAt", "posted_at")


@post_type.field("category")
async def resolve_category(obj: Post, info: GraphQLResolveInfo) -> Category:
    category = await load_category(info.context, obj.category_id)
    return cast(Category, category)


@post_type.field("thread")
async def resolve_thread(obj: Post, info: GraphQLResolveInfo) -> Thread:
    thread = await load_thread(info.context, obj.thread_id)
    return cast(Thread, thread)


@post_type.field("poster")
async def resolve_poster(obj: Post, info: GraphQLResolveInfo) -> Optional[User]:
    if obj.poster_id:
        return await load_user(info.context, obj.poster_id)
    return None
