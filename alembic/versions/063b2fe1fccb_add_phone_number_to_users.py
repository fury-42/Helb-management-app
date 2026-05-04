"""add phone number to users

Revision ID: 063b2fe1fccb
Revises: d28bc5152e54
Create Date: 2026-05-04 19:00:39.179062

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '063b2fe1fccb'
down_revision: Union[str, Sequence[str], None] = 'd28bc5152e54'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('users', sa.Column('phone_number', sa.String(), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('users', 'phone_number')
