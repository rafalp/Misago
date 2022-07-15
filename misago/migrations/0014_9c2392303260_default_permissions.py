"""default_permissions

Revision ID: 9c2392303260
Revises: 02a349a35f04
Create Date: 2022-07-15 19:03:04.123093

"""
from alembic import op
from sqlalchemy import Integer, String
from sqlalchemy.sql import column, table

from misago.categories.models import CategoryType


# revision identifiers, used by Alembic.
revision = "9c2392303260"
down_revision = "02a349a35f04"
branch_labels = None
depends_on = None

# tables
permissions = table(
    "misago_user_groups_permissions",
    column("group_id", Integer),
    column("permission", String(length=50)),
)

category_permissions = table(
    "misago_categories_permissions",
    column("group_id", Integer),
    column("category_id", Integer),
    column("permission", String(length=50)),
)


# permissions
default_permissions = {
    "administrators": [],
    "moderators": [],
    "members": [],
    "guests": [],
}

default_category_permissions = {
    "administrators": ["SEE", "READ", "START", "REPLY", "UPLOAD", "DOWNLOAD"],
    "moderators": ["SEE", "READ", "START", "REPLY", "UPLOAD", "DOWNLOAD"],
    "members": ["SEE", "READ", "START", "REPLY", "UPLOAD", "DOWNLOAD"],
    "guests": ["SEE", "READ", "DOWNLOAD"],
}


def upgrade():
    conn = op.get_bind()

    groups = conn.execute("SELECT id, slug FROM misago_user_groups").fetchall()
    categories = conn.execute("SELECT id, type FROM misago_categories").fetchall()

    permissions_data = []
    category_permissions_data = []

    for group_id, group_slug in groups:
        for permission in default_permissions[group_slug]:
            permissions_data.append({"group_id": group_id, "permission": permission})

        for category_id, category_type in categories:
            if category_type != CategoryType.THREADS:
                continue

            for permission in default_category_permissions[group_slug]:
                category_permissions_data.append(
                    {
                        "group_id": group_id,
                        "category_id": category_id,
                        "permission": permission,
                    }
                )

    op.bulk_insert(permissions, permissions_data)
    op.bulk_insert(category_permissions, category_permissions_data)


def downgrade():
    pass
