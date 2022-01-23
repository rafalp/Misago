import pytest

from ..categories.models import Category


@pytest.fixture
async def categories(db):
    top_category = await Category.create(name="Category", left=3, right=6)
    child_category = await Category.create(
        name="Child Category", parent=top_category, left=4, right=5, depth=1
    )
    sibling_category = await Category.create(name="Sibling Category", left=7, right=8)
    closed_category = await Category.create(
        name="Closed Category", left=9, right=10, is_closed=True
    )
    return (top_category, child_category, sibling_category, closed_category)


@pytest.fixture
def category(categories):
    return categories[0]


@pytest.fixture
def child_category(categories):
    return categories[1]


@pytest.fixture
def sibling_category(categories):
    return categories[2]


@pytest.fixture
def closed_category(categories):
    return categories[3]
