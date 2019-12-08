"""default_settings

Revision ID: 69d552c761f2
Revises: ad2a1d098a41
Create Date: 2019-11-17 01:49:55.824480

"""
from datetime import timedelta

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column
from sqlalchemy import JSON, String

from misago.utils.strings import get_random_string


settings = [
    {"name": "forum_name", "value": "Misago"},
    {"name": "jwt_exp", "value": int(timedelta(days=90).total_seconds())},
    {"name": "jwt_secret", "value": get_random_string(64)},
    {"name": "password_min_length", "value": 8},
    {"name": "username_min_length", "value": 3},
    {"name": "username_max_length", "value": 10},
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
