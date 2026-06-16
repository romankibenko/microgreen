"""add sort_order to products

Revision ID: f5a6b7c8d9e0
Revises: e4f5a6b7c8d9
Create Date: 2026-06-16 21:00:00.000000

"""
from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f5a6b7c8d9e0'
down_revision: str | None = 'e4f5a6b7c8d9'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        'products',
        sa.Column(
            'sort_order',
            sa.Integer(),
            nullable=False,
            server_default='0',
        ),
    )


def downgrade() -> None:
    op.drop_column('products', 'sort_order')
