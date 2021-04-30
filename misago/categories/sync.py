from asyncio import gather

from .models import Category


async def sync_category(category: Category) -> Category:
    threads_count, posts_count = await gather(
        category.threads_query.count(),
        category.posts_query.count(),
    )

    return await category.update(threads=threads_count, posts=posts_count)
