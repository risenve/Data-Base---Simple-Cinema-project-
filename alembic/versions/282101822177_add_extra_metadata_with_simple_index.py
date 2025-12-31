"""Add extra_metadata with simple index

Revision ID: 282101822177
Revises: 5e01b905ce59
Create Date: 2025-12-31 13:10:41.781953

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '282101822177'
down_revision: Union[str, Sequence[str], None] = '5e01b905ce59'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
