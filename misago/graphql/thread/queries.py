from typing import Awaitable, Optional

from ariadne_graphql_modules import ObjectType, gql
from graphql import GraphQLResolveInfo

from ...threads.loaders import threads_loader
from ...threads.models import Thread
from ..args import clean_id_arg, handle_invalid_args
from ..connection import ConnectionResult
from .connection import ThreadConnectionType, thread_connection
from .thread import ThreadType


class ThreadQueries(ObjectType):
    __schema__ = gql(
        """
        type Query {
            threads(before: ID, after: ID, first: Int, last: Int, category: ID, user: ID): ThreadConnection
            thread(id: ID!): Thread
        }
        """
    )
    __requires__ = [
        ThreadConnectionType,
        ThreadType,
    ]

    @staticmethod
    @handle_invalid_args
    async def resolve_threads(
        _,
        info: GraphQLResolveInfo,
        *,
        after: Optional[str] = None,
        before: Optional[str] = None,
        first: Optional[int] = None,
        last: Optional[int] = None,
        category: Optional[int] = None,
        user: Optional[str] = None
    ) -> ConnectionResult:
        category_id = clean_id_arg(category) if category else None
        starter_id = clean_id_arg(user) if user else None

        categories_index = info.context["categories"]
        if category_id:
            categories = categories_index.get_children_ids(
                category_id, include_parent=True
            )
        else:
            categories = categories_index.all_ids

        threads_query = Thread.query.filter(category_id__in=categories)
        if starter_id:
            threads_query = threads_query.filter(starter_id=starter_id)

        return await thread_connection.resolve(
            info.context,
            threads_query,
            {
                "after": after,
                "before": before,
                "first": first,
                "last": last,
            },
            info.context["settings"]["threads_per_page"],
        )

    @staticmethod
    @handle_invalid_args
    def resolve_thread(
        _, info: GraphQLResolveInfo, *, id: str  # pylint: disable=redefined-builtin
    ) -> Awaitable[Optional[Thread]]:
        thread_id = clean_id_arg(id)
        return threads_loader.load(info.context, thread_id)
