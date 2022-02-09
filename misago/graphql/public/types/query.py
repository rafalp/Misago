from typing import Awaitable, List, Optional

from ariadne import QueryType
from graphql import GraphQLResolveInfo

from ....categories.models import Category
from ....loaders import (
    load_categories,
    load_category_with_children,
    load_forum_stats,
    load_root_categories,
    load_user,
)
from ....richtext import RichText, parse_markup
from ....threads.get import get_threads_page
from ....threads.loaders import posts_loader, threads_loader
from ....threads.models import Post, Thread, ThreadsFeed
from ....users.models import User
from ...cleanargs import (
    clean_graphql_id,
    clean_graphql_cursor,
    clean_graphql_cursors,
    invalid_args_result,
)

query_type = QueryType()


@query_type.field("auth")
def resolve_auth(_, info: GraphQLResolveInfo) -> Optional[User]:
    return info.context["user"]


@query_type.field("categories")
def resolve_categories(_, info: GraphQLResolveInfo) -> Awaitable[List[Category]]:
    return load_root_categories(info.context)


@query_type.field("category")
@invalid_args_result
async def resolve_category(
    _, info: GraphQLResolveInfo, *, id: str  # pylint: disable=redefined-builtin
) -> Optional[Category]:
    category_id = clean_graphql_id(id)

    # Load all categories so we can aggregate their stats
    categories = await load_categories(info.context)

    # Search for category
    for category in categories:
        if category.id == category_id:
            return category

    return None


@query_type.field("thread")
@invalid_args_result
def resolve_thread(
    _, info: GraphQLResolveInfo, *, id: str  # pylint: disable=redefined-builtin
) -> Awaitable[Optional[Thread]]:
    thread_id = clean_graphql_id(id)
    return threads_loader.load(info.context, thread_id)


@query_type.field("threads")
@invalid_args_result
async def resolve_threads(
    _,
    info: GraphQLResolveInfo,
    *,
    after: Optional[str] = None,
    before: Optional[str] = None,
    category: Optional[str] = None,
    user: Optional[str] = None
) -> Awaitable[ThreadsFeed]:
    after, before = clean_graphql_cursors(after, before)
    category_id = clean_graphql_id(category)
    starter_id = clean_graphql_id(user)

    if category_id:
        categories = await load_category_with_children(info.context, category_id)
    else:
        categories = await load_categories(info.context)

    return await get_threads_page(
        info.context["settings"]["threads_per_page"],
        after=after,
        before=before,
        starter_id=starter_id,
        categories_ids=[category.id for category in categories],
    )


@query_type.field("post")
@invalid_args_result
def resolve_post(
    _, info: GraphQLResolveInfo, *, id: str  # pylint: disable=redefined-builtin
) -> Awaitable[Optional[Post]]:
    post_id = clean_graphql_id(id)
    return posts_loader.load(info.context, post_id)


@query_type.field("posts")
@invalid_args_result
async def resolve_posts(
    _, info: GraphQLResolveInfo, *, thread: str, page: int = 1
) -> Optional[Post]:
    thread_id = clean_graphql_id(thread)
    page = clean_graphql_cursor(page)

    paginator = await posts_loader.load_paginator(info.context, thread_id)
    if not paginator:
        return None

    return await paginator.get_page(page)


@query_type.field("user")
@invalid_args_result
def resolve_user(
    _, info: GraphQLResolveInfo, *, id: str  # pylint: disable=redefined-builtin
) -> Awaitable[Optional[User]]:
    user_id = clean_graphql_id(id)
    return load_user(info.context, user_id)


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
