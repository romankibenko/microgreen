"""add harvested_to_site to plantings

Revision ID: a7b8c9d0e1f2
Revises: f5a6b7c8d9e0
Create Date: 2026-07-07 00:00:00.000000

"""
from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a7b8c9d0e1f2'
down_revision: str | None = 'f5a6b7c8d9e0'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        'plantings', sa.Column('harvested_to_site', sa.Integer(), nullable=True)
    )
    # у уже собранных партий весь урожай считаем ушедшим на сайт (как было раньше)
    op.execute(
        'UPDATE plantings SET harvested_to_site = harvested_qty '
        'WHERE harvested_qty IS NOT NULL'
    )
    op.create_check_constraint(
        'ck_plantings_harvested_to_site_valid',
        'plantings',
        'harvested_to_site IS NULL '
        'OR (harvested_to_site >= 0 AND harvested_to_site <= harvested_qty)',
    )


def downgrade() -> None:
    op.drop_constraint(
        'ck_plantings_harvested_to_site_valid', 'plantings', type_='check'
    )
    op.drop_column('plantings', 'harvested_to_site')
