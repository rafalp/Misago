"""default_settings

Revision ID: 69d552c761f2
Revises: ad2a1d098a41
Create Date: 2019-11-17 01:49:55.824480

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column
from sqlalchemy import JSON, String


settings = [
    {"name": "forum_name", "value": "Misago"},
]

table = table("misago_settings", column("name", String), column("value", JSON),)

# revision identifiers, used by Alembic.
revision = "69d552c761f2"
down_revision = "ad2a1d098a41"
branch_labels = None
depends_on = None


def upgrade():
    op.bulk_insert(table, settings)


def downgrade():
    pass
