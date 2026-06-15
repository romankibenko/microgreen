"""add shade_days to plantings

Revision ID: c2d3e4f5a6b7
Revises: b1c2d3e4f5a6
Create Date: 2026-06-13 00:00:00.000000

"""
from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c2d3e4f5a6b7'
down_revision: str | None = 'b1c2d3e4f5a6'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        'plantings',
        sa.Column('shade_days', sa.Integer(), nullable=False, server_default='3'),
    )
    op.create_check_constraint(
        'ck_plantings_shade_days_valid',
        'plantings',
        'shade_days >= 0 AND shade_days <= grow_days',
    )


def downgrade() -> None:
    op.drop_constraint('ck_plantings_shade_days_valid', 'plantings', type_='check')
    op.drop_column('plantings', 'shade_days')
