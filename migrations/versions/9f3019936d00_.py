"""empty message

Revision ID: 9f3019936d00
Revises: a2ca783d3962
Create Date: 2017-02-08 18:11:59.539471

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9f3019936d00'
down_revision = 'a2ca783d3962'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'first_name',
               existing_type=sa.VARCHAR(length=20),
               nullable=True)
    op.alter_column('user', 'last_name',
               existing_type=sa.VARCHAR(length=20),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'last_name',
               existing_type=sa.VARCHAR(length=20),
               nullable=False)
    op.alter_column('user', 'first_name',
               existing_type=sa.VARCHAR(length=20),
               nullable=False)
    # ### end Alembic commands ###
