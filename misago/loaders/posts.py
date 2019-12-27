from typing import Awaitable, Iterable, Optional, Sequence, Union

from ..types import GraphQLContext, Post
from ..threads.get import get_posts_by_id
from .loader import get_loader


def load_post(
    context: GraphQLContext, post_id: Union[int, str]
) -> Awaitable[Optional[Post]]:
    loader = get_loader(context, "post_loader", get_posts_by_id)
    return loader.load(post_id)


def load_posts(
    context: GraphQLContext, ids: Sequence[Union[int, str]]
) -> Awaitable[Sequence[Optional[Post]]]:
    loader = get_loader(context, "post_loader", get_posts_by_id)
    return loader.load_many(ids)


def store_post(context: GraphQLContext, post: Post):
    loader = get_loader(context, "post_loader", get_posts_by_id)
    loader.clear(post.id)
    loader.prime(post.id, post)


def store_posts(context: GraphQLContext, posts: Iterable[Post]):
    loader = get_loader(context, "post_loader", get_posts_by_id)
    for post in posts:
        loader.clear(post.id)
        loader.prime(post.id, post)


def clear_post(context: GraphQLContext, post: Post):
    loader = get_loader(context, "post_loader", get_posts_by_id)
    loader.clear(post.id)


def clear_posts(context: GraphQLContext, posts: Iterable[Post]):
    loader = get_loader(context, "post_loader", get_posts_by_id)
    for post in posts:
        loader.clear(post.id)


def clear_all_posts(context: GraphQLContext):
    loader = get_loader(context, "post_loader", get_posts_by_id)
    loader.clear_all()
