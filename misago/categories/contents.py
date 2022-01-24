from asyncio import gather
from typing import Iterable

from ..threads.models import Post, Thread
from .hooks import delete_categories_contents_hook, move_categories_contents_hook
from .models import Category

__all__ = ["delete_categories_contents", "move_categories_contents"]


async def move_categories_contents(
    categories: Iterable[Category], new_category: Category
):
    await move_categories_contents_hook.call_action(
        _move_categories_contents_action, categories, new_category
    )


async def _move_categories_contents_action(
    categories: Iterable[Category], new_category: Category
):
    categories_ids = [c.id for c in categories]
    threads_query = Thread.query.filter(category_id__in=categories_ids).update(
        category_id=new_category.id,
    )
    posts_query = Post.query.filter(category_id__in=categories_ids).update(
        category_id=new_category.id,
    )

    await gather(threads_query, posts_query)


async def delete_categories_contents(categories: Iterable[Category]):
    await delete_categories_contents_hook.call_action(
        _delete_categories_contents_action, categories
    )


async def _delete_categories_contents_action(categories: Iterable[Category]):
    await Thread.query.filter(category_id__in=[c.id for c in categories]).delete()
