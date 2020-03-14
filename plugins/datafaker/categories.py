import random
from typing import Optional

from faker import Faker
from misago.types import Category
from misago.categories.create import create_category
from misago.categories.get import get_categories_mptt
from misago.categories.update import update_category


async def create_fake_category(
    fake: Faker, *, parent: Optional[Category] = None
) -> Category:
    categories = await get_categories_mptt()
    categories_map = {c.id: c for c in categories.nodes()}

    new_category = await create_category(
        name=get_fake_category_name(fake), parent=parent,
    )
    categories.insert_node(new_category, parent)
    categories_map[new_category.id] = new_category

    updated_categories = {}
    for category in categories.nodes():
        if category.parent_id:
            parent = updated_categories[category.parent_id]
        else:
            parent = False

        updated_categories[category.id] = await update_category(
            categories_map[category.id],
            parent=parent,
            left=category.left,
            right=category.right,
            depth=category.depth,
            is_closed=random.randint(1, 100) > 80,
        )

    return updated_categories[new_category.id]


def get_fake_category_name(fake: Faker) -> str:
    if random.randint(1, 100) > 75:
        return fake.catch_phrase().title()
    return fake.street_name()
