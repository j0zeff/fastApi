"""Added isDeleted column to Users table

Revision ID: 9b94dd624f2a
Revises: d1dab86ff6bb
Create Date: 2024-07-25 11:42:59.771468

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "9b94dd624f2a"
down_revision: Union[str, None] = "d1dab86ff6bb"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "Users",
        sa.Column(
            "isDeleted", sa.Boolean(), server_default=sa.text("true"), nullable=False
        ),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("Users", "isDeleted")
    # ### end Alembic commands ###
