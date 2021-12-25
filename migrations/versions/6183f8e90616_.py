"""empty message

Revision ID: 6183f8e90616
Revises: f5353fc7cb15
Create Date: 2021-12-24 22:42:17.371460

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6183f8e90616'
down_revision = 'f5353fc7cb15'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.add_column(sa.Column('category_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key('post', 'category', ['category_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('category_id')

    # ### end Alembic commands ###