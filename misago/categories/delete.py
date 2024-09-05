from .models import Category


def delete_category(category: Category):
    category.delete()
