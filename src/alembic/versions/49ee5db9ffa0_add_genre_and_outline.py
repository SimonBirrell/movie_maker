"""add genre and outline

Revision ID: 49ee5db9ffa0
Revises: 341bc8c57255
Create Date: 2024-07-26 09:47:23.626010

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '49ee5db9ffa0'
down_revision: Union[str, None] = '341bc8c57255'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('movie_projects', sa.Column('genre', sa.String(50), nullable=True))
    op.add_column('movie_projects', sa.Column('outline', sa.Text, nullable=True))


def downgrade() -> None:
    op.drop_column('movie_projects', 'genre')
    op.drop_column('movie_projects', 'outline')
