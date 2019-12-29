from typing import Awaitable, Iterable, Optional, Sequence, Union

from ..types import GraphQLContext, Post, Thread, ThreadPostsPage
from ..threads.get import get_posts_by_id, get_thread_posts_page
from .loader import get_loader


def load_post(
    context: GraphQLContext, post_id: Union[int, str]
) -> Awaitable[Optional[Post]]:
    loader = get_loader(context, "post", get_posts_by_id)
    return loader.load(post_id)


def load_posts(
    context: GraphQLContext, ids: Sequence[Union[int, str]]
) -> Awaitable[Sequence[Optional[Post]]]:
    loader = get_loader(context, "post", get_posts_by_id)
    return loader.load_many(ids)


async def load_thread_posts_page(
    context: GraphQLContext, thread: Thread, page: int
) -> Optional[ThreadPostsPage]:
    posts_page = await get_thread_posts_page(
        thread,
        context["settings"]["posts_per_page"],
        context["settings"]["posts_per_page_orphans"],
        page,
    )
    if posts_page:
        store_posts(context, posts_page.items)
    return posts_page


def store_post(context: GraphQLContext, post: Post):
    loader = get_loader(context, "post", get_posts_by_id)
    loader.clear(post.id)
    loader.prime(post.id, post)


def store_posts(context: GraphQLContext, posts: Iterable[Post]):
    loader = get_loader(context, "post", get_posts_by_id)
    for post in posts:
        loader.clear(post.id)
        loader.prime(post.id, post)


def clear_post(context: GraphQLContext, post: Post):
    loader = get_loader(context, "post", get_posts_by_id)
    loader.clear(post.id)


def clear_posts(context: GraphQLContext, posts: Iterable[Post]):
    loader = get_loader(context, "post", get_posts_by_id)
    for post in posts:
        loader.clear(post.id)


def clear_all_posts(context: GraphQLContext):
    loader = get_loader(context, "post", get_posts_by_id)
    loader.clear_all()
