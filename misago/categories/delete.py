from ..postgres.delete import delete_many, delete_one
from .models import Category


def delete_category(category: Category):
    _delete_category_action(category)


def _delete_category_action(category: Category):
    delete_one(category)
