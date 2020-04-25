from typing import List, Optional

from ariadne import QueryType
from graphql import GraphQLResolveInfo

from ...auth import get_authenticated_user
from ...loaders import (
    load_categories,
    load_category,
    load_category_with_children,
    load_forum_stats,
    load_root_categories,
    load_thread,
    load_threads_feed,
    load_updated_threads_count,
    load_user,
)
from ...types import Category, Settings, Thread, ThreadsFeed, User


query_type = QueryType()


@query_type.field("auth")
async def resolve_auth(_, info: GraphQLResolveInfo) -> Optional[User]:
    return await get_authenticated_user(info.context)


@query_type.field("categories")
async def resolve_categories(_, info: GraphQLResolveInfo) -> List:
    return await load_root_categories(info.context)


@query_type.field("category")
async def resolve_category(
    _, info: GraphQLResolveInfo, *, id: str  # pylint: disable=redefined-builtin
) -> Optional[Category]:
    return await load_category(info.context, id)


@query_type.field("thread")
async def resolve_thread(
    _, info: GraphQLResolveInfo, *, id: str  # pylint: disable=redefined-builtin
) -> Optional[Thread]:
    return await load_thread(info.context, id)


@query_type.field("threads")
async def resolve_threads(
    _,
    info: GraphQLResolveInfo,
    *,
    cursor: Optional[str] = None,
    category: Optional[str] = None,
    user: Optional[str] = None
) -> Optional[ThreadsFeed]:
    if category:
        categories = await load_category_with_children(info.context, category)
    else:
        categories = await load_categories(info.context)

    return await load_threads_feed(
        info.context, categories=categories, cursor=cursor, starter_id=user
    )


@query_type.field("updatedThreads")
async def resolve_updated_threads(
    _,
    info: GraphQLResolveInfo,
    *,
    cursor: str,
    category: Optional[str] = None,
    user: Optional[str] = None
) -> int:
    if category:
        categories = await load_category_with_children(info.context, category)
    else:
        categories = await load_categories(info.context)

    return await load_updated_threads_count(
        info.context, cursor, categories=categories, starter_id=user
    )


@query_type.field("user")
async def resolve_user(
    _, info: GraphQLResolveInfo, *, id: str  # pylint: disable=redefined-builtin
) -> Optional[User]:
    return await load_user(info.context, id)


@query_type.field("forumStats")
async def resolve_forum_stats(_, info: GraphQLResolveInfo) -> dict:
    return await load_forum_stats(info.context)


@query_type.field("settings")
def resolve_settings(_, info: GraphQLResolveInfo) -> Settings:
    return info.context["settings"]
