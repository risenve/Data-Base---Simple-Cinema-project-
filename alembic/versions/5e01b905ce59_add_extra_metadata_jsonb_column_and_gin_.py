
"""Add extra_metadata JSONB column and GIN index to events

Revision ID: 5e01b905ce59
Revises: d79bc3da18de  # <-- ID предыдущей миграции
Create Date: 2024-01-15 10:30:00.000000

"""

from alembic import op
import sqlalchemy as sa

revision = '5e01b905ce59'
down_revision = 'd79bc3da18de'
branch_labels = None
depends_on = None

def upgrade():
    op.add_column('events', sa.Column('extra_metadata', sa.JSON(), nullable=True))
    
    
    op.execute("""
        CREATE INDEX ix_events_extra_metadata_gin 
        ON events 
        USING gin ((extra_metadata::text) gin_trgm_ops)
    """)

def downgrade():
    op.drop_index('ix_events_extra_metadata_gin', table_name='events')
    op.drop_column('events', 'extra_metadata')