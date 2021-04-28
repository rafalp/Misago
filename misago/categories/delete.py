from ..database.queries import delete
from ..tables import categories
from .models import Category


async def delete_category(category: Category):
    await delete(categories, category.id)
