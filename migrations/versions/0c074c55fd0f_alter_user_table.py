"""Alter User Table

Revision ID: 0c074c55fd0f
Revises: a02f24daf4a9
Create Date: 2024-01-02 15:13:05.800639

"""
from typing import Sequence, Union
import sqlmodel
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0c074c55fd0f'
down_revision: Union[str, None] = 'a02f24daf4a9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'user', ['email'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user', type_='unique')
    # ### end Alembic commands ###
