"""Trying to fix bugs

Revision ID: b21830de2e69
Revises: 7719290aceaa
Create Date: 2023-03-05 19:30:34.932181

"""
from alembic import op
import sqlalchemy as sa


revision = 'b21830de2e69'
down_revision = '7719290aceaa'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('product_lists', sa.Column('user_id', sa.BigInteger(), nullable=False))
    op.create_foreign_key(None, 'product_lists', 'users', ['user_id'], ['id'])
    op.add_column('users', sa.Column('seller_id', sa.BigInteger(), nullable=True))
    op.create_foreign_key(None, 'users', 'sellers', ['seller_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='foreignkey')
    op.drop_column('users', 'seller_id')
    op.drop_constraint(None, 'product_lists', type_='foreignkey')
    op.drop_column('product_lists', 'user_id')
    # ### end Alembic commands ###
