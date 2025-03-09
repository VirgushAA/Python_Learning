"""Description of changes

Add 'speed' column to spaceships table

Revision ID: 893e9b1ba723
Revises:
Create Date: 2025-02-19 18:44:27.973529

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'add_speed'  # 893e9b1ba723
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('spaceships', sa.Column('speed', sa.Integer, nullable=True))


def downgrade() -> None:
    op.drop_column('spaceships', 'speed')
