"""defaullt_groups

Revision ID: 59c5ea8d68aa
Revises: 543a72fd396e
Create Date: 2022-07-10 21:30:57.218518

"""
from typing import List

from alembic import op
from sqlalchemy import JSON, Boolean, Integer, String
from sqlalchemy.sql import column, table


# revision identifiers, used by Alembic.
revision = "59c5ea8d68aa"
down_revision = "543a72fd396e"
branch_labels = None
depends_on = None


table = table(
    "misago_user_groups",
    column("name", String(length=255)),
    column("slug", String(length=255)),
    column("order", Integer),
    column("is_default", Boolean),
    column("is_moderator", Boolean),
    column("is_admin", Boolean),
    column("permissions", JSON),
)


user_groups: List[dict] = [
    {
        "name": "Administrators",
        "slug": "administrators",
        "order": 0,
        "is_default": False,
        "is_moderator": True,
        "is_admin": True,
        "permissions": {},
    },
    {
        "name": "Moderators",
        "slug": "Moderators",
        "order": 1,
        "is_default": False,
        "is_moderator": True,
        "is_admin": False,
        "permissions": {},
    },
    {
        "name": "Members",
        "slug": "members",
        "order": 2,
        "is_default": True,
        "is_moderator": False,
        "is_admin": False,
        "permissions": {},
    },
]


def upgrade():
    op.bulk_insert(table, user_groups)


def downgrade():
    pass
