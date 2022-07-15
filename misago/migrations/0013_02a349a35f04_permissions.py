"""permissions

Revision ID: 02a349a35f04
Revises: 86a1f6e142b5
Create Date: 2022-07-15 18:33:18.128502

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "02a349a35f04"
down_revision = "86a1f6e142b5"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "misago_categories_permissions",
        sa.Column("id", sa.BigInteger(), nullable=False),
        sa.Column("group_id", sa.BigInteger(), nullable=False),
        sa.Column("category_id", sa.Integer(), nullable=False),
        sa.Column("permission", sa.String(length=50), nullable=False),
        sa.ForeignKeyConstraint(
            ["category_id"], ["misago_categories.id"], ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(
            ["group_id"], ["misago_user_groups.id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "misago_user_groups_permissions",
        sa.Column("id", sa.BigInteger(), nullable=False),
        sa.Column("group_id", sa.BigInteger(), nullable=False),
        sa.Column("permission", sa.String(length=50), nullable=False),
        sa.ForeignKeyConstraint(
            ["group_id"], ["misago_user_groups.id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("misago_user_groups_permissions")
    op.drop_table("misago_categories_permissions")
    # ### end Alembic commands ###
