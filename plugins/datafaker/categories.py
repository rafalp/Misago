import random
from typing import Dict, Optional, cast

from faker import Faker

from misago.types import Category
from misago.categories.create import create_category
from misago.categories.get import get_all_categories
from misago.categories.tree import insert_category
from misago.categories.update import update_category


async def create_fake_category(
    fake: Faker, *, parent: Optional[Category] = None
) -> Category:
    all_categories = await get_all_categories()
    new_category = await create_category(
        name=get_fake_category_name(fake), parent=parent,
    )
    return await insert_category(all_categories, new_category, parent)


def get_fake_category_name(fake: Faker) -> str:
    if random.randint(1, 100) > 75:
        return fake.catch_phrase().title()
    return fake.street_name()
