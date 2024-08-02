"""create cast_members table

Revision ID: 8c2095aa1a84
Revises: 49ee5db9ffa0
Create Date: 2024-08-02 10:30:33.189812

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8c2095aa1a84'
down_revision: Union[str, None] = '49ee5db9ffa0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'cast_members',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('movie_project_id', sa.Integer, sa.ForeignKey('movie_projects.id')),
        sa.Column('character_name', sa.String(50), nullable=False),
        sa.Column('actor_name', sa.String(50), nullable=False),
        sa.Column('justification_for_actor', sa.Unicode(200)),
    )


def downgrade() -> None:
    op.drop_table('cast_members')
