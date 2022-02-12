from typing import Awaitable, Optional, cast

from ariadne import ObjectType
from graphql import GraphQLResolveInfo

from ....categories.loaders import categories_loader
from ....categories.models import Category
from ....threads.loaders import posts_loader
from ....threads.models import Post, Thread
from ....users.loaders import users_loader
from ....users.models import User
from ...cleanargs import clean_id_arg, invalid_args_handler

thread_type = ObjectType("Thread")

thread_type.set_alias("starterName", "starter_name")
thread_type.set_alias("lastPosterName", "last_poster_name")
thread_type.set_alias("startedAt", "started_at")
thread_type.set_alias("lastPostedAt", "last_posted_at")
thread_type.set_alias("isClosed", "is_closed")


@thread_type.field("category")
def resolve_category(obj: Thread, info: GraphQLResolveInfo) -> Awaitable[Category]:
    category = categories_loader.load(info.context, obj.category_id)
    return cast(Awaitable[Category], category)


@thread_type.field("firstPost")
def resolve_first_post(
    obj: Thread, info: GraphQLResolveInfo
) -> Optional[Awaitable[Optional[Post]]]:
    if obj.first_post_id:
        return posts_loader.load(info.context, obj.first_post_id)
    return None


@thread_type.field("starter")
async def resolve_starter(obj: Thread, info: GraphQLResolveInfo) -> Optional[User]:
    if obj.starter_id:
        starter = await users_loader.load(info.context, obj.starter_id)
        if starter and starter.is_active:
            return starter
    return None


@thread_type.field("lastPost")
def resolve_last_post(
    obj: Thread, info: GraphQLResolveInfo
) -> Optional[Awaitable[Optional[Post]]]:
    if obj.last_post_id:
        return posts_loader.load(info.context, obj.last_post_id)
    return None


@thread_type.field("lastPoster")
async def resolve_last_poster(obj: Thread, info: GraphQLResolveInfo) -> Optional[User]:
    if obj.last_poster_id:
        last_poster = await users_loader.load(info.context, obj.last_poster_id)
        if last_poster and last_poster.is_active:
            return last_poster
    return None


@thread_type.field("post")
@invalid_args_handler
async def resolve_post(
    obj: Thread,
    info: GraphQLResolveInfo,
    *,
    id: str,  # pylint: disable=redefined-builtin
) -> Optional[Post]:
    post_id = clean_id_arg(id)
    post = await posts_loader.load(info.context, post_id)
    if post and post.thread_id == obj.id:
        return post
    return None
