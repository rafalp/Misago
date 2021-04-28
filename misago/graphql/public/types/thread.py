from typing import Awaitable, Optional, cast

from ariadne import ObjectType
from graphql import GraphQLResolveInfo

from ....categories.models import Category
from ....database.paginator import Paginator
from ....loaders import (
    load_category,
    load_post,
    load_thread_post_url,
    load_thread_posts_paginator,
    load_user,
)
from ....threads.models import Post, Thread
from ....users.models import User

thread_type = ObjectType("Thread")

thread_type.set_alias("starterName", "starter_name")
thread_type.set_alias("lastPosterName", "last_poster_name")
thread_type.set_alias("startedAt", "started_at")
thread_type.set_alias("lastPostedAt", "last_posted_at")
thread_type.set_alias("isClosed", "is_closed")


@thread_type.field("category")
def resolve_category(obj: Thread, info: GraphQLResolveInfo) -> Awaitable[Category]:
    category = load_category(info.context, obj.category_id)
    return cast(Awaitable[Category], category)


@thread_type.field("posts")
def resolve_posts(obj: Thread, info: GraphQLResolveInfo) -> Awaitable[Paginator]:
    return load_thread_posts_paginator(info.context, obj)


@thread_type.field("firstPost")
def resolve_first_post(
    obj: Thread, info: GraphQLResolveInfo
) -> Optional[Awaitable[Optional[Post]]]:
    if obj.first_post_id:
        return load_post(info.context, obj.first_post_id)
    return None


@thread_type.field("starter")
async def resolve_starter(obj: Thread, info: GraphQLResolveInfo) -> Optional[User]:
    if obj.starter_id:
        starter = await load_user(info.context, obj.starter_id)
        if starter and starter.is_active:
            return starter
    return None


@thread_type.field("lastPost")
def resolve_last_post(
    obj: Thread, info: GraphQLResolveInfo
) -> Optional[Awaitable[Optional[Post]]]:
    if obj.last_post_id:
        return load_post(info.context, obj.last_post_id)
    return None


@thread_type.field("lastPoster")
async def resolve_last_poster(obj: Thread, info: GraphQLResolveInfo) -> Optional[User]:
    if obj.last_poster_id:
        last_poster = await load_user(info.context, obj.last_poster_id)
        if last_poster and last_poster.is_active:
            return last_poster
    return None


@thread_type.field("lastPostUrl")
async def resolve_last_post_url(
    obj: Thread,
    info: GraphQLResolveInfo,
    *,
    absolute: bool = False,
) -> Optional[str]:
    if obj.last_post_id:
        post = await load_post(info.context, obj.last_post_id)
        if post:
            return await load_thread_post_url(info.context, obj, post, absolute)
    return None


@thread_type.field("post")
async def resolve_post(
    obj: Thread,
    info: GraphQLResolveInfo,
    *,
    id: str,  # pylint: disable=redefined-builtin
) -> Optional[Post]:
    post = await load_post(info.context, id)
    if post and post.thread_id == obj.id:
        return post
    return None


@thread_type.field("postUrl")
async def resolve_post_url(
    obj: Thread,
    info: GraphQLResolveInfo,
    *,
    id: str,  # pylint: disable=redefined-builtin
    absolute: bool = False,
) -> Optional[str]:
    if obj.last_post_id:
        post = await load_post(info.context, id)
        if post and post.thread_id == obj.id:
            return await load_thread_post_url(info.context, obj, post, absolute)
    return None
