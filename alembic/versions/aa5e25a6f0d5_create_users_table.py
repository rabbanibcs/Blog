"""create users table

Revision ID: aa5e25a6f0d5
Revises: 
Create Date: 2022-10-14 03:59:36.604525

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.expression import text

# revision identifiers, used by Alembic.
revision = 'aa5e25a6f0d5'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id",sa.Integer,primary_key=True),
        sa.Column("name",sa.String,nullable=True),
        sa.Column("email",sa.String,unique=True),
        sa.Column("password",sa.String),
        sa.Column("created_at",sa.TIMESTAMP(timezone=True),server_default=text('now()'))
    )


def downgrade() -> None:
    op.drop_table("users")
