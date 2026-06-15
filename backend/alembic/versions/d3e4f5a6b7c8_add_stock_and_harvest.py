"""add stock to products and harvest fields to plantings

Revision ID: d3e4f5a6b7c8
Revises: c2d3e4f5a6b7
Create Date: 2026-06-15 00:00:00.000000

"""
from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd3e4f5a6b7c8'
down_revision: str | None = 'c2d3e4f5a6b7'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        'products',
        sa.Column('stock', sa.Integer(), nullable=False, server_default='0'),
    )
    op.create_check_constraint(
        'ck_products_stock_non_negative', 'products', 'stock >= 0'
    )
    op.add_column('plantings', sa.Column('harvested_at', sa.Date(), nullable=True))
    op.add_column('plantings', sa.Column('harvested_qty', sa.Integer(), nullable=True))
    op.create_check_constraint(
        'ck_plantings_harvested_qty_positive',
        'plantings',
        'harvested_qty IS NULL OR harvested_qty > 0',
    )


def downgrade() -> None:
    op.drop_constraint(
        'ck_plantings_harvested_qty_positive', 'plantings', type_='check'
    )
    op.drop_column('plantings', 'harvested_qty')
    op.drop_column('plantings', 'harvested_at')
    op.drop_constraint('ck_products_stock_non_negative', 'products', type_='check')
    op.drop_column('products', 'stock')
