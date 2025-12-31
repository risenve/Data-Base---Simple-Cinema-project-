from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB

revision = 'новая_дата_вставьте_сюда'
down_revision = '5e01b905ce59'

def upgrade():
    op.add_column('events', sa.Column('extra_metadata', JSONB(), nullable=True))
    
    op.create_index('ix_events_extra_metadata', 'events', ['extra_metadata'])

def downgrade():
    op.drop_index('ix_events_extra_metadata', table_name='events')
    op.drop_column('events', 'extra_metadata')
