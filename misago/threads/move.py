from asyncio import gather
from dataclasses import replace
from typing import List, Iterable

from ..categories.models import Category
from .models import Post, Thread


async def move_thread(thread: Thread, new_category: Category) -> Thread:
    if thread.category_id == new_category.id:
        return thread

    thread, _ = await gather(
        thread.update(category=new_category),
        thread.posts_query.update(category_id=new_category.id),
    )

    return thread


async def move_threads(
    threads: Iterable[Thread], new_category: Category
) -> List[Thread]:
    updated_threads: List[Thread] = []
    threads_ids: List[int] = []

    for thread in threads:
        if thread.category_id != new_category.id:
            thread = replace(thread, category_id=new_category.id)
            threads_ids.append(thread.id)
            updated_threads.append(thread)

    if threads_ids:
        move_threads_query = Thread.query.filter(id__in=threads_ids).update(
            category_id=new_category.id
        )
        move_posts_query = Post.query.filter(thread_id__in=threads_ids).update(
            category_id=new_category.id
        )
        await gather(move_threads_query, move_posts_query)

    return updated_threads


async def move_categories_threads(
    categories: Iterable[Category], new_category: Category
):
    categories_ids = [c.id for c in categories]
    move_threads_query = Thread.query.filter(category_id__in=categories_ids).update(
        category_id=new_category.id
    )
    move_posts_query = Post.query.filter(category_id__in=categories_ids).update(
        category_id=new_category.id
    )

    await gather(move_threads_query, move_posts_query)
