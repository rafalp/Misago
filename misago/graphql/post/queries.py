from typing import Awaitable, Optional

from ariadne_graphql_modules import ObjectType, gql
from graphql import GraphQLResolveInfo

from ...database.paginator import Page
from ...threads.loaders import posts_loader
from ...threads.models import Post
from ..args import (
    clean_id_arg,
    clean_page_arg,
    handle_invalid_args,
)
from .post import PostType
from .postspage import PostsPageType
from .resolvers import resolve_posts_page


class PostQueries(ObjectType):
    __schema__ = gql(
        """
        type Query {
            posts(thread: ID!, page: Int): PostsPage
            post(id: ID!): Post
        }
        """
    )
    __requires__ = [
        PostType,
        PostsPageType,
    ]

    @staticmethod
    @handle_invalid_args
    async def resolve_posts(
        _, info: GraphQLResolveInfo, *, thread: str, page: int = 1
    ) -> Optional[Page]:
        thread_id = clean_id_arg(thread)
        page = clean_page_arg(page)

        return resolve_posts_page(info, thread_id, page=page)

    @staticmethod
    @handle_invalid_args
    def resolve_post(
        _, info: GraphQLResolveInfo, *, id: str  # pylint: disable=redefined-builtin
    ) -> Awaitable[Optional[Post]]:
        post_id = clean_id_arg(id)
        return posts_loader.load(info.context, post_id)
