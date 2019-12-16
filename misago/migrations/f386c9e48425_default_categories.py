"""default_categories

Revision ID: f386c9e48425
Revises: 05180e3cdd4b
Create Date: 2019-12-15 21:51:27.434952

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import Integer, JSON, String
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
    column("extra", JSON),
)


categories = [
    {
        # id: 1
        "type": CategoryTypes.THREADS,
        "parent_id": None,
        "depth": 0,
        "left": 1,
        "right": 6,
        "name": "Hobbies",
        "slug": "hobbies",
        "extra": {},
    },
    {
        # id: 2
        "type": CategoryTypes.THREADS,
        "parent_id": 1,
        "depth": 1,
        "left": 2,
        "right": 3,
        "name": "Books",
        "slug": "books",
        "extra": {},
    },
    {
        # id: 3
        "type": CategoryTypes.THREADS,
        "parent_id": None,
        "depth": 1,
        "left": 4,
        "right": 5,
        "name": "Movies",
        "slug": "movies",
        "extra": {},
    },
]


def upgrade():
    op.bulk_insert(table, categories)


def downgrade():
    pass
