"""Added Users table

Revision ID: 786a6591bb78
Revises: 9f26b5ff5deb
Create Date: 2024-07-17 13:07:37.295202

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '786a6591bb78'
down_revision: Union[str, None] = '9f26b5ff5deb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('password_hash', sa.String(), nullable=False),
    sa.Column('access_token', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_Users_id'), 'Users', ['id'], unique=False)
    op.create_index(op.f('ix_Users_username'), 'Users', ['username'], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_Users_username'), table_name='Users')
    op.drop_index(op.f('ix_Users_id'), table_name='Users')
    op.drop_table('Users')
    # ### end Alembic commands ###