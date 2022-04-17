from typing import Awaitable, Optional, cast

from ariadne import ObjectType
from graphql import GraphQLResolveInfo

from ....categories.loaders import categories_loader
from ....categories.models import Category
from ....richtext.html import convert_rich_text_to_html
from ....threads.loaders import posts_loader, threads_loader
from ....threads.models import Post, Thread
from ....users.loaders import users_loader
from ....users.models import User
from ....utils.request import create_absolute_url

post_type = ObjectType("Post")

post_type.set_alias("posterName", "poster_name")
post_type.set_alias("postedAt", "posted_at")
post_type.set_alias("richText", "rich_text")


@post_type.field("category")
def resolve_category(obj: Post, info: GraphQLResolveInfo) -> Awaitable[Category]:
    category = categories_loader.load(info.context, obj.category_id)
    return cast(Awaitable[Category], category)


@post_type.field("thread")
def resolve_thread(obj: Post, info: GraphQLResolveInfo) -> Awaitable[Thread]:
    thread = threads_loader.load(info.context, obj.thread_id)
    return cast(Awaitable[Thread], thread)


@post_type.field("poster")
async def resolve_poster(obj: Post, info: GraphQLResolveInfo) -> Optional[User]:
    if obj.poster_id:
        poster = await users_loader.load(info.context, obj.poster_id)
        if poster and poster.is_active:
            return poster
    return None


@post_type.field("html")
def resolve_html(obj: Post, info: GraphQLResolveInfo) -> str:
    return convert_rich_text_to_html(info.context, obj.rich_text)


@post_type.field("url")
async def resolve_url(
    obj: Post, info: GraphQLResolveInfo, *, absolute: bool = False
) -> str:
    url = cast(str, await posts_loader.load_url(info.context, obj))
    if absolute:
        return create_absolute_url(info.context["request"], url)

    return url
