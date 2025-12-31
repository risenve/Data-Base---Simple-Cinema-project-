"""add_indexes_for_search

Revision ID: 4c087ffb4360
Revises: 4fa454f951ac
Create Date: 2025-12-31 15:53:59.239253

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4c087ffb4360'
down_revision: Union[str, Sequence[str], None] = '4fa454f951ac'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
