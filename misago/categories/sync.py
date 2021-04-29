from asyncio import gather

from .models import Category
from .update import update_category


async def sync_category(category: Category) -> Category:
    threads_count, posts_count = await gather(
        category.threads_query.count(),
        category.posts_query.count(),
    )

    return await update_category(category, threads=threads_count, posts=posts_count)
