from typing import Awaitable, Optional, cast

from ariadne import ObjectType
from graphql import GraphQLResolveInfo

from ...database.paginator import Paginator
from ...loaders import (
    load_category,
    load_post,
    load_thread_post_url,
    load_thread_posts_paginator,
    load_user,
)
from ...types import Category, Post, Thread, User
from ...utils.request import get_absolute_url


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
def resolve_starter(
    obj: Thread, info: GraphQLResolveInfo
) -> Optional[Awaitable[Optional[User]]]:
    if obj.starter_id:
        return load_user(info.context, obj.starter_id)
    return None


@thread_type.field("lastPost")
def resolve_last_post(
    obj: Thread, info: GraphQLResolveInfo
) -> Optional[Awaitable[Optional[Post]]]:
    if obj.last_post_id:
        return load_post(info.context, obj.last_post_id)
    return None


@thread_type.field("lastPoster")
def resolve_last_poster(
    obj: Thread, info: GraphQLResolveInfo
) -> Optional[Awaitable[Optional[User]]]:
    if obj.last_poster_id:
        return load_user(info.context, obj.last_poster_id)
    return None


@thread_type.field("lastPostUrl")
async def resolve_last_post_url(
    obj: Thread, info: GraphQLResolveInfo, *, absolute: bool = False,
) -> Optional[str]:
    if obj.last_post_id:
        post = await load_post(info.context, obj.last_post_id)
        if post:
            return await get_post_url(info, obj, post, absolute)
    return None


@thread_type.field("post")
async def resolve_post(
    obj: Thread,
    info: GraphQLResolveInfo,
    *,
    id: str,  # pylint: disable=redefined-builtin
) -> Awaitable[Optional[Post]]:
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
            return await get_post_url(info, obj, post, absolute)
    return None


async def get_post_url(
    info: GraphQLResolveInfo, thread: Thread, post: Post, absolute: bool
) -> str:
    url = await load_thread_post_url(info.context, thread, post)
    if absolute:
        return get_absolute_url(info.context["request"], url)
    return url
