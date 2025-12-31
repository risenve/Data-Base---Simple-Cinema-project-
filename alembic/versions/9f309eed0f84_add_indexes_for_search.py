"""add_indexes_for_search

Revision ID: 9f309eed0f84
Revises: 4c087ffb4360
Create Date: 2025-12-31 16:17:56.028048

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9f309eed0f84'
down_revision: Union[str, Sequence[str], None] = '4c087ffb4360'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
