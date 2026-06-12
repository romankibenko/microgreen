"""add trays to plantings

Revision ID: b1c2d3e4f5a6
Revises: 8b3e7c2a1f94
Create Date: 2026-06-12 00:00:00.000000

"""
from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b1c2d3e4f5a6'
down_revision: str | None = '8b3e7c2a1f94'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        'plantings',
        sa.Column('trays', sa.Integer(), nullable=False, server_default='1'),
    )
    op.create_check_constraint('ck_plantings_trays_positive', 'plantings', 'trays > 0')


def downgrade() -> None:
    op.drop_constraint('ck_plantings_trays_positive', 'plantings', type_='check')
    op.drop_column('plantings', 'trays')
