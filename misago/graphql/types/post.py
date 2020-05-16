from typing import Awaitable, Optional, cast

from ariadne import ObjectType
from graphql import GraphQLResolveInfo

from ...loaders import load_category, load_thread, load_user
from ...types import Category, Post, Thread, User


post_type = ObjectType("Post")

post_type.set_alias("posterName", "poster_name")
post_type.set_alias("postedAt", "posted_at")


@post_type.field("category")
def resolve_category(obj: Post, info: GraphQLResolveInfo) -> Awaitable[Category]:
    category = load_category(info.context, obj.category_id)
    return cast(Awaitable[Category], category)


@post_type.field("thread")
def resolve_thread(obj: Post, info: GraphQLResolveInfo) -> Awaitable[Thread]:
    thread = load_thread(info.context, obj.thread_id)
    return cast(Awaitable[Thread], thread)


@post_type.field("poster")
def resolve_poster(
    obj: Post, info: GraphQLResolveInfo
) -> Optional[Awaitable[Optional[User]]]:
    if obj.poster_id:
        return load_user(info.context, obj.poster_id)
    return None
