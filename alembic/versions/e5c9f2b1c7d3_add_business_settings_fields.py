"""add business settings fields

Revision ID: e5c9f2b1c7d3
Revises: df09fe7b129f
Create Date: 2026-03-26 10:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e5c9f2b1c7d3'
down_revision: Union[str, Sequence[str], None] = 'df09fe7b129f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('businesses', sa.Column('currency', sa.String(length=10), nullable=True))
    op.add_column('businesses', sa.Column('tax_percent', sa.Float(), nullable=True))
    op.add_column('businesses', sa.Column('receipt_footer', sa.String(length=500), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('businesses', 'receipt_footer')
    op.drop_column('businesses', 'tax_percent')
    op.drop_column('businesses', 'currency')
