from typing import Optional, cast

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
async def resolve_category(obj: Thread, info: GraphQLResolveInfo) -> Category:
    category = await load_category(info.context, obj.category_id)
    return cast(Category, category)


@thread_type.field("posts")
async def resolve_posts(
    obj: Thread, info: GraphQLResolveInfo, page: int = 1
) -> Optional[ThreadPostsPage]:
    return await load_thread_posts_page(info.context, obj, page)


@thread_type.field("firstPost")
async def resolve_first_post(obj: Thread, info: GraphQLResolveInfo) -> Optional[Post]:
    if obj.first_post_id:
        return await load_post(info.context, obj.first_post_id)
    return None


@thread_type.field("starter")
async def resolve_starter(obj: Thread, info: GraphQLResolveInfo) -> Optional[User]:
    if obj.starter_id:
        return await load_user(info.context, obj.starter_id)
    return None


@thread_type.field("lastPost")
async def resolve_last_post(obj: Thread, info: GraphQLResolveInfo) -> Optional[Post]:
    if obj.last_post_id:
        return await load_post(info.context, obj.last_post_id)
    return None


@thread_type.field("lastPoster")
async def resolve_last_poster(obj: Thread, info: GraphQLResolveInfo) -> Optional[User]:
    if obj.last_poster_id:
        return await load_user(info.context, obj.last_poster_id)
    return None
