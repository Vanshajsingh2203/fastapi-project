
"""Create books table.

Revision ID: a6c92f14b7e1
Revises: 0dec57d8dfb0
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "a6c92f14b7e1"
down_revision: Union[str, Sequence[str], None] = "0dec57d8dfb0"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "books",
        sa.Column("uid", postgresql.UUID(), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("author", sa.String(), nullable=False),
        sa.Column("publisher", sa.String(), nullable=False),
        sa.Column("published_date", sa.Date(), nullable=False),
        sa.Column("page_count", sa.Integer(), nullable=False),
        sa.Column("language", sa.String(), nullable=False),
        sa.Column("created_at", postgresql.TIMESTAMP(), nullable=True),
        sa.Column("updated_at", postgresql.TIMESTAMP(), nullable=True),
        sa.PrimaryKeyConstraint("uid"),
    )


def downgrade() -> None:
    op.drop_table("books")
