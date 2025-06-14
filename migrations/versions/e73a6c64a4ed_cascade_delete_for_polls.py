"""Cascade delete for polls

Revision ID: e73a6c64a4ed
Revises: 7be6bf3f70d9
Create Date: 2025-06-10 22:40:30.891653

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'e73a6c64a4ed'
down_revision: Union[str, None] = '7be6bf3f70d9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tickets')
    op.add_column('options', sa.Column('votes_count', sa.Integer(), nullable=True))
    op.drop_column('options', 'votes')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('options', sa.Column('votes', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_column('options', 'votes_count')
    op.create_table('tickets',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('title', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('description', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('status', postgresql.ENUM('open', 'in_progress', 'closed', name='ticketstatus'), autoincrement=False, nullable=False),
    sa.Column('priority', postgresql.ENUM('low', 'medium', 'high', name='ticketpriority'), autoincrement=False, nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(), server_default=sa.text('now()'), autoincrement=False, nullable=True),
    sa.Column('updated_at', postgresql.TIMESTAMP(), server_default=sa.text('now()'), autoincrement=False, nullable=True),
    sa.Column('owner_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['owner_id'], ['users.id'], name='tickets_owner_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='tickets_pkey')
    )
    # ### end Alembic commands ###
