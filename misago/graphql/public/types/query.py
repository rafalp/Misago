from typing import Awaitable, List, Optional

from ariadne import QueryType
from graphql import GraphQLResolveInfo

from ....categories.get import get_categories
from ....categories.loaders import categories_loader
from ....categories.models import Category
from ....database.paginator import Page
from ....forumstats.loaders import load_forum_stats
from ....richtext import RichText, parse_markup
from ....threads.get import ThreadsPage, get_threads_page
from ....threads.loaders import posts_loader, threads_loader
from ....threads.models import Post, Thread
from ....users.loaders import users_loader
from ....users.models import User
from ...cleanargs import (
    clean_cursors_args,
    clean_id_arg,
    clean_page_arg,
    invalid_args_handler,
)

query_type = QueryType()


@query_type.field("auth")
def resolve_auth(_, info: GraphQLResolveInfo) -> Optional[User]:
    return info.context["user"]


@query_type.field("category")
@invalid_args_handler
def resolve_category(
    _, info: GraphQLResolveInfo, *, id: str  # pylint: disable=redefined-builtin
) -> Awaitable[Optional[Category]]:
    category_id = clean_id_arg(id)
    return categories_loader.load(info.context, category_id)


@query_type.field("categories")
@invalid_args_handler
def resolve_categories(*_, parent: Optional[int] = None) -> Awaitable[List[Category]]:
    parent_id = clean_id_arg(parent) if parent else None
    return get_categories(parent_id=parent_id)


@query_type.field("thread")
@invalid_args_handler
def resolve_thread(
    _, info: GraphQLResolveInfo, *, id: str  # pylint: disable=redefined-builtin
) -> Awaitable[Optional[Thread]]:
    thread_id = clean_id_arg(id)
    return threads_loader.load(info.context, thread_id)


@query_type.field("threads")
@invalid_args_handler
async def resolve_threads(
    _,
    info: GraphQLResolveInfo,
    *,
    after: Optional[str] = None,
    before: Optional[str] = None,
    category: Optional[str] = None,
    user: Optional[str] = None
) -> ThreadsPage:
    after_cursor, before_cursor = clean_cursors_args(after, before)
    category_id = clean_id_arg(category) if category else None
    starter_id = clean_id_arg(user) if user else None

    categories_index = info.context["categories"]
    if category_id:
        categories = categories_index.get_children_ids(category_id, include_parent=True)
    else:
        categories = categories_index.all_ids

    return await get_threads_page(
        info.context["settings"]["threads_per_page"],
        after=after_cursor,
        before=before_cursor,
        starter_id=starter_id,
        categories_ids=categories,
    )


@query_type.field("post")
@invalid_args_handler
def resolve_post(
    _, info: GraphQLResolveInfo, *, id: str  # pylint: disable=redefined-builtin
) -> Awaitable[Optional[Post]]:
    post_id = clean_id_arg(id)
    return posts_loader.load(info.context, post_id)


@query_type.field("posts")
@invalid_args_handler
async def resolve_posts(
    _, info: GraphQLResolveInfo, *, thread: str, page: int = 1
) -> Optional[Page]:
    thread_id = clean_id_arg(thread)
    page = clean_page_arg(page)

    paginator = await posts_loader.load_paginator(info.context, thread_id)
    if not paginator:
        return None

    return await paginator.get_page(page)


@query_type.field("user")
@invalid_args_handler
def resolve_user(
    _, info: GraphQLResolveInfo, *, id: str  # pylint: disable=redefined-builtin
) -> Awaitable[Optional[User]]:
    user_id = clean_id_arg(id)
    return users_loader.load(info.context, user_id)


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
