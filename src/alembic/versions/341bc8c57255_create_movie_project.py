"""create movie_project

Revision ID: 341bc8c57255
Revises: 
Create Date: 2024-07-24 10:41:26.458489

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '341bc8c57255'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "movie_projects",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("title", sa.String, index=True),
        sa.Column("description", sa.String),
        sa.Column("budget", sa.Integer, default=0),
    )


def downgrade() -> None:
    op.drop_table("movie_projects")
