"""default_categories

Revision ID: f386c9e48425
Revises: 05180e3cdd4b
Create Date: 2019-12-15 21:51:27.434952

"""
from typing import List

from alembic import op
from sqlalchemy import Boolean, Integer, JSON, String
from sqlalchemy.sql import table, column

from misago.categories.categorytypes import CategoryTypes


# revision identifiers, used by Alembic.
revision = "f386c9e48425"
down_revision = "05180e3cdd4b"
branch_labels = None
depends_on = None

# default data
table = table(
    "misago_categories",
    column("type", Integer),
    column("parent_id", Integer),
    column("depth", Integer),
    column("left", Integer),
    column("right", Integer),
    column("name", String(length=255)),
    column("slug", String(length=255)),
    column("is_closed", Boolean),
    column("extra", JSON),
)


categories: List[dict] = [
    {
        # id: 1
        "type": CategoryTypes.PRIVATE_THREADS,
        "parent_id": None,
        "depth": 0,
        "left": 1,
        "right": 2,
        "name": "PRIVATE_THREADS",
        "slug": "private-threads",
        "is_closed": False,
        "extra": {},
    },
    {
        # id: 2
        "type": CategoryTypes.THREADS,
        "parent_id": None,
        "depth": 0,
        "left": 1,
        "right": 2,
        "name": "Example category",
        "slug": "example-category",
        "is_closed": False,
        "extra": {},
    },
]


def upgrade():
    op.bulk_insert(table, categories)


def downgrade():
    pass
