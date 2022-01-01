from typing import Awaitable, List, Optional

from ariadne import QueryType
from graphql import GraphQLResolveInfo

from ....categories.models import Category
from ....loaders import (
    load_categories,
    load_category,
    load_category_with_children,
    load_forum_stats,
    load_post,
    load_categories,
    load_thread,
    load_threads_feed,
    load_user,
)
from ....richtext import RichText, parse_markup
from ....threads.models import Post, Thread, ThreadsFeed
from ....users.models import User

query_type = QueryType()


@query_type.field("auth")
def resolve_auth(_, info: GraphQLResolveInfo) -> Optional[User]:
    return info.context["user"]


@query_type.field("categories")
def resolve_categories(_, info: GraphQLResolveInfo) -> Awaitable[List[Category]]:
    return load_categories(info.context)


@query_type.field("category")
def resolve_category(
    _, info: GraphQLResolveInfo, *, id: str  # pylint: disable=redefined-builtin
) -> Awaitable[Optional[Category]]:
    # Load all categories so we can aggregate their stats
    categories = load_categories(info.context)

    # Search for category
    for category in categories:
        if str(category.id) == id:
            return category
    
    return None


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


@query_type.field("richText")
async def resolve_rich_text(_, info: GraphQLResolveInfo, *, markup: str) -> RichText:
    rich_text, _ = await parse_markup(info.context, markup)
    return rich_text
