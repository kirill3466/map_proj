"""Add votes table

Revision ID: f2bc05dc6677
Revises: 5c97a9d62d9c
Create Date: 2025-06-10 13:26:21.418157

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f2bc05dc6677'
down_revision: Union[str, None] = '5c97a9d62d9c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'votes',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('poll_id', sa.Integer(), sa.ForeignKey("polls.id")),
        sa.Column('option_id', sa.Integer(), sa.ForeignKey("options.id")),
        sa.Column('user_identifier', sa.String(), index=True)
    )


def downgrade():
    op.drop_table('votes')
