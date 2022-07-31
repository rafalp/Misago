"""enable_trigam

Revision ID: 0378e1db4b09
Revises: 69d552c761f2
Create Date: 2022-07-10 21:26:13.415627

"""
from alembic import op


# revision identifiers, used by Alembic.
revision = "0378e1db4b09"
down_revision = "69d552c761f2"
branch_labels = None
depends_on = None


def upgrade():
    op.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm;")


def downgrade():
    pass
