"""Added isDeleted column to Users table

Revision ID: d1dab86ff6bb
Revises: 786a6591bb78
Create Date: 2024-07-25 11:31:05.079163

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "d1dab86ff6bb"
down_revision: Union[str, None] = "786a6591bb78"
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
