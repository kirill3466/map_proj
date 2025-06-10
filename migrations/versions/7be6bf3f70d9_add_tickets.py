"""Add tickets

Revision ID: 7be6bf3f70d9
Revises: f2bc05dc6677
Create Date: 2025-06-10 14:33:27.618645

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7be6bf3f70d9'
down_revision: Union[str, None] = 'f2bc05dc6677'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'tickets',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=False),
        sa.Column('status', sa.Enum('open', 'in_progress', 'closed', name='ticketstatus'), nullable=False, default='open'),
        sa.Column('priority', sa.Enum('low', 'medium', 'high', name='ticketpriority'), nullable=False, default='medium'),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.func.now(), onupdate=sa.func.now()),
        sa.Column('owner_id', sa.Integer(), sa.ForeignKey('users.id')),
    )


def downgrade():
    op.drop_table('tickets')
    sa.Enum(name='ticketstatus').drop(op.get_bind())
    sa.Enum(name='ticketpriority').drop(op.get_bind())
