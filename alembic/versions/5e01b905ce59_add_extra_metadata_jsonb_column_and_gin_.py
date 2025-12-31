"""Add extra_metadata JSONB column and GIN index to events

Revision ID: 5e01b905ce59
Revises: d79bc3da18de
Create Date: 2024-01-15 10:30:00.000000

"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB

# revision identifiers, used by Alembic.
revision = '5e01b905ce59'
down_revision = 'd79bc3da18de'
branch_labels = None
depends_on = None


def upgrade():
    """Upgrade schema."""
    op.add_column('events', sa.Column('extra_metadata', JSONB(), nullable=True))
    
    op.execute('CREATE INDEX ix_events_extra_metadata ON events USING gin (extra_metadata jsonb_path_ops);')
    
    # op.create_index('ix_events_extra_metadata', 'events', ['extra_metadata'])


def downgrade():
    """Downgrade schema."""
    op.drop_index('ix_events_extra_metadata', table_name='events')
    op.drop_column('events', 'extra_metadata')
