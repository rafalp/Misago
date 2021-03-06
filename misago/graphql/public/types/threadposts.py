from typing import Awaitable, Optional

from ariadne import ObjectType
from graphql import GraphQLResolveInfo

from ....database.paginator import Paginator
from ....loaders import load_thread_posts_page
from ....types import ThreadPostsPage

thread_posts_type = ObjectType("ThreadPosts")


@thread_posts_type.field("page")
def resolve_page(
    obj: Paginator, info: GraphQLResolveInfo, page: int = 1
) -> Awaitable[Optional[ThreadPostsPage]]:
    return load_thread_posts_page(info.context, obj, page)


@thread_posts_type.field("pagination")
def resolve_pagination(obj: Paginator, info: GraphQLResolveInfo) -> Paginator:
    return obj
