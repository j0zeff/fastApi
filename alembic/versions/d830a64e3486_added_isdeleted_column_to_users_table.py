"""Added isDeleted column to Users table

Revision ID: d830a64e3486
Revises: 9b94dd624f2a
Create Date: 2024-07-25 12:42:06.978060

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "d830a64e3486"
down_revision: Union[str, None] = "9b94dd624f2a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
