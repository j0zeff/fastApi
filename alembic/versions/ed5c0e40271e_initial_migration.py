"""Initial migration

Revision ID: ed5c0e40271e
Revises: 
Create Date: 2024-07-11 13:39:58.049951

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "ed5c0e40271e"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "ParameterType",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=50), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "ProductionParameters",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=50), nullable=True),
        sa.Column("code", sa.Integer(), nullable=True),
        sa.Column("parentCode", sa.Integer(), nullable=True),
        sa.Column("parameterTypeId", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["parameterTypeId"],
            ["ParameterType.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("ProductionParameters")
    op.drop_table("ParameterType")
    # ### end Alembic commands ###
