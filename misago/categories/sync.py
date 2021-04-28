from ..database.queries import count
from ..tables import posts, threads
from .models import Category
from .update import update_category


async def sync_category(category: Category) -> Category:
    return await update_category(
        category,
        threads=await count(
            threads.select().where(threads.c.category_id == category.id)
        ),
        posts=await count(posts.select().where(posts.c.category_id == category.id)),
    )
