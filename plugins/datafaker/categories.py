import random
from typing import Optional

from faker import Faker

from misago.categories.create import create_category
from misago.categories.get import get_all_categories
from misago.categories.models import Category
from misago.categories.tree import insert_category


async def create_fake_category(
    fake: Faker, *, parent: Optional[Category] = None
) -> Category:
    all_categories = await get_all_categories()
    new_category = await create_category(
        name=get_fake_category_name(fake),
        color=fake.color(luminosity="light"),
        parent=parent,
    )
    category, _ = await insert_category(all_categories, new_category, parent)
    return category


def get_fake_category_name(fake: Faker) -> str:
    if random.randint(1, 100) > 75:
        return fake.catch_phrase().title()
    return fake.street_name()
