"""Add extra_metadata JSONB column and GIN index to events

Revision ID: 5e01b905ce59
Revises: d79bc3da18de
Create Date: 2025-12-31 03:39:04.424608

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5e01b905ce59'
down_revision: Union[str, Sequence[str], None] = 'd79bc3da18de'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.add_column('events', sa.Column('extra_metadata', postgresql.JSONB(), nullable=True))
    op.create_index('ix_events_extra_metadata', 'events', ['extra_metadata'], postgresql_using='gin')

def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index('ix_events_extra_metadata_gin', table_name='events')
    op.drop_column('events', 'extra_metadata')
