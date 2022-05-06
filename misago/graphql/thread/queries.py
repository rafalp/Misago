from typing import Awaitable, Optional

from ariadne_graphql_modules import ObjectType, gql
from graphql import GraphQLResolveInfo

from ...threads.get import ThreadsPage, get_threads_page
from ...threads.loaders import threads_loader
from ...threads.models import Thread
from ..args import (
    clean_cursors_args,
    clean_id_arg,
    handle_invalid_args,
)
from .thread import ThreadType
from .threadspage import ThreadsPageType


class ThreadQueries(ObjectType):
    __schema__ = gql(
        """
        type Query {
            threads(before: ID, after: ID, category: ID, user: ID): ThreadsPage
            thread(id: ID!): Thread
        }
        """
    )
    __requires__ = [
        ThreadType,
        ThreadsPageType,
    ]

    @staticmethod
    @handle_invalid_args
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
            categories = categories_index.get_children_ids(
                category_id, include_parent=True
            )
        else:
            categories = categories_index.all_ids

        return await get_threads_page(
            info.context["settings"]["threads_per_page"],
            after=after_cursor,
            before=before_cursor,
            starter_id=starter_id,
            categories_ids=categories,
        )

    @staticmethod
    @handle_invalid_args
    def resolve_thread(
        _, info: GraphQLResolveInfo, *, id: str  # pylint: disable=redefined-builtin
    ) -> Awaitable[Optional[Thread]]:
        thread_id = clean_id_arg(id)
        return threads_loader.load(info.context, thread_id)
