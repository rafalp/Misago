from typing import Awaitable, List, Optional

from ariadne import QueryType
from graphql import GraphQLResolveInfo

from ...auth import get_authenticated_user
from ...loaders import (
    load_categories,
    load_category,
    load_category_with_children,
    load_forum_stats,
    load_post,
    load_root_categories,
    load_thread,
    load_threads_feed,
    load_user,
)
from ...richtext import parse_markup
from ...types import Category, Post, RichText, Settings, Thread, ThreadsFeed, User


query_type = QueryType()


@query_type.field("auth")
def resolve_auth(_, info: GraphQLResolveInfo) -> Awaitable[Optional[User]]:
    return get_authenticated_user(info.context)


@query_type.field("categories")
def resolve_categories(_, info: GraphQLResolveInfo) -> Awaitable[List[Category]]:
    return load_root_categories(info.context)


@query_type.field("category")
def resolve_category(
    _, info: GraphQLResolveInfo, *, id: str  # pylint: disable=redefined-builtin
) -> Awaitable[Optional[Category]]:
    return load_category(info.context, id)


@query_type.field("thread")
def resolve_thread(
    _, info: GraphQLResolveInfo, *, id: str  # pylint: disable=redefined-builtin
) -> Awaitable[Optional[Thread]]:
    return load_thread(info.context, id)


@query_type.field("post")
def resolve_post(
    _, info: GraphQLResolveInfo, *, id: str  # pylint: disable=redefined-builtin
) -> Awaitable[Optional[Post]]:
    return load_post(info.context, id)


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


@query_type.field("user")
def resolve_user(
    _, info: GraphQLResolveInfo, *, id: str  # pylint: disable=redefined-builtin
) -> Awaitable[Optional[User]]:
    return load_user(info.context, id)


@query_type.field("search")
def resolve_search(
    _, info: GraphQLResolveInfo, *, query: str  # pylint: disable=redefined-builtin
) -> str:
    return query.strip()


@query_type.field("forumStats")
def resolve_forum_stats(_, info: GraphQLResolveInfo) -> Awaitable[dict]:
    return load_forum_stats(info.context)


@query_type.field("settings")
def resolve_settings(_, info: GraphQLResolveInfo) -> Settings:
    return info.context["settings"]


@query_type.field("richText")
def resolve_rich_text(_, info: GraphQLResolveInfo, *, markup: str) -> RichText:
    return parse_markup(info.context, markup)
