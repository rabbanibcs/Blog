"""add a column to users

Revision ID: 1147b98bb64a
Revises: aa5e25a6f0d5
Create Date: 2022-10-15 14:48:02.160742

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1147b98bb64a'
down_revision = 'aa5e25a6f0d5'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("users",sa.Column("fname",sa.String(50),nullable=True))


def downgrade() -> None:
    # op.drop_column
    op.drop_column("users","fname")
