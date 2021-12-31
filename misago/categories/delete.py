from .models import Category


async def delete_category(category: Category):
    await category.delete()
