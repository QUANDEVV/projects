"""NEW

Revision ID: 1d952da8471c
Revises: bdc7289351a6
Create Date: 2023-06-07 21:14:45.530428

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1d952da8471c'
down_revision = 'bdc7289351a6'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('passengers', sa.Column('username', sa.String(), nullable=True))
    op.add_column('passengers', sa.Column('password', sa.String(), nullable=True))
    op.create_unique_constraint(None, 'passengers', ['username'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'passengers', type_='unique')
    op.drop_column('passengers', 'password')
    op.drop_column('passengers', 'username')
    # ### end Alembic commands ###