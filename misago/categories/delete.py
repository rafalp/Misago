from ..database.queries import delete
from ..tables import categories
from ..types import Category


async def delete_category(category: Category):
    await delete(categories, category.id)
