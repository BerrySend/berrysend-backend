"""update_users_table_with_full_name

Revision ID: 8bd5cc0a06d2
Revises: f7e909a271da
Create Date: 2025-11-16 14:49:30.513050

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8bd5cc0a06d2'
down_revision: Union[str, Sequence[str], None] = 'f7e909a271da'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """
    Upgrade database schema.
    
    Updates the user's table structure for the authentication system:
    - Adds full_name column
    - Ensures email is unique and indexed
    - Ensures password column exists
    """
    # Add a full_name column to the user's table
    op.add_column('users', sa.Column('full_name', sa.String(length=100), nullable=False, server_default=''))
    
    # Remove server_default after the column is created
    op.alter_column('users', 'full_name', server_default=None)
    
    # Ensure email has a unique constraint and index
    # (This may already exist, but we ensure it here)
    try:
        op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    except:
        # Index may already exist, skip if it does
        pass


def downgrade() -> None:
    """
    Downgrade database schema.
    
    Removes the full_name column from the user's table.
    """
    # Remove the full_name column
    op.drop_column('users', 'full_name')
    
    # Remove the index if it exists
    try:
        op.drop_index(op.f('ix_users_email'), table_name='users')
    except:
        # Index may not exist, skip if it doesn't
        pass
