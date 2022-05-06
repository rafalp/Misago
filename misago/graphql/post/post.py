from typing import Awaitable, Optional, cast

from ariadne_graphql_modules import DeferredType, ObjectType, gql
from graphql import GraphQLResolveInfo

from ...categories.loaders import categories_loader
from ...categories.models import Category
from ...richtext.html import convert_rich_text_to_html
from ...threads.loaders import posts_loader, threads_loader
from ...threads.models import Post, Thread
from ...users.loaders import users_loader
from ...users.models import User
from ...utils.request import create_absolute_url
from ..richtext import RichTextScalar
from ..scalars import DateTimeScalar, GenericScalar


class PostType(ObjectType):
    __schema__ = gql(
        """
        type Post {
            id: ID!
            category: Category!
            thread: Thread!
            poster: User
            posterName: String!
            markup: String!
            richText: RichText!
            html: String!
            edits: Int!
            postedAt: DateTime!
            url(absolute: Boolean): String!
            extra: Generic!
        }
        """
    )
    __aliases__ = {
        "posterName": "poster_name",
        "richText": "rich_text",
        "postedAt": "posted_at",
    }
    __requires__ = [
        DeferredType("Category"),
        DeferredType("Thread"),
        DeferredType("User"),
        DateTimeScalar,
        GenericScalar,
        RichTextScalar,
    ]

    @staticmethod
    def resolve_category(obj: Post, info: GraphQLResolveInfo) -> Awaitable[Category]:
        category = categories_loader.load(info.context, obj.category_id)
        return cast(Awaitable[Category], category)

    @staticmethod
    def resolve_thread(obj: Post, info: GraphQLResolveInfo) -> Awaitable[Thread]:
        thread = threads_loader.load(info.context, obj.thread_id)
        return cast(Awaitable[Thread], thread)

    @staticmethod
    async def resolve_poster(obj: Post, info: GraphQLResolveInfo) -> Optional[User]:
        if obj.poster_id:
            poster = await users_loader.load(info.context, obj.poster_id)
            if poster and poster.is_active:
                return poster
        return None

    @staticmethod
    def resolve_html(obj: Post, info: GraphQLResolveInfo) -> str:
        return convert_rich_text_to_html(info.context, obj.rich_text)

    @staticmethod
    async def resolve_url(
        obj: Post, info: GraphQLResolveInfo, *, absolute: bool = False
    ) -> str:
        url = cast(str, await posts_loader.load_url(info.context, obj))
        if absolute:
            return create_absolute_url(info.context["request"], url)

        return url
