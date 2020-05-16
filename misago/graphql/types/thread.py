from typing import Awaitable, Optional, cast

from ariadne import ObjectType
from graphql import GraphQLResolveInfo

from ...loaders import load_category, load_post, load_thread_posts_page, load_user
from ...types import Category, Post, Thread, ThreadPostsPage, User


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
def resolve_posts(
    obj: Thread, info: GraphQLResolveInfo, page: int = 1
) -> Awaitable[Optional[ThreadPostsPage]]:
    return load_thread_posts_page(info.context, obj, page)


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
