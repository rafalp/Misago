"""default_categories

Revision ID: ca7ed91ca363
Revises: 9ea4f438f320
Create Date: 2022-07-10 21:34:31.228445

"""
from typing import List

from alembic import op
from sqlalchemy import JSON, Boolean, Integer, String
from sqlalchemy.sql import column, table

from misago.categories.models import CategoryType


# revision identifiers, used by Alembic.
revision = "ca7ed91ca363"
down_revision = "9ea4f438f320"
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
        "type": CategoryType.PRIVATE_THREADS,
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
        "type": CategoryType.THREADS,
        "parent_id": None,
        "depth": 0,
        "left": 1,
        "right": 2,
        "name": "Example category",
        "slug": "example-category",
        "color": "#FF5630",
        "is_closed": False,
        "extra": {},
    },
]


def upgrade():
    op.bulk_insert(table, categories)


def downgrade():
    pass
