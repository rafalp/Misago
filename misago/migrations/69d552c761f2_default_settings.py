"""default_settings

Revision ID: 69d552c761f2
Revises: ad2a1d098a41
Create Date: 2019-11-17 01:49:55.824480

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column
from sqlalchemy import String, Text


settings = [
    {"name": "forum_name", "value": "Misago"},
]

settings_table = table(
    "misago_settings",
    column("name", String),
    column("python_type", String),
    column("value", Text),
)

# revision identifiers, used by Alembic.
revision = "69d552c761f2"
down_revision = "ad2a1d098a41"
branch_labels = None
depends_on = None


def upgrade():
    data = []
    for setting in settings:
        setting.setdefault("python_type", "string")
        data.append(setting)

    op.bulk_insert(settings_table, data)


def downgrade():
    pass
