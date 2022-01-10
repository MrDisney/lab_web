"""empty message

Revision ID: e8024913cc6e
Revises: 6183f8e90616
Create Date: 2022-01-10 18:42:41.078124

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e8024913cc6e'
down_revision = '6183f8e90616'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('subject',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name_subject', sa.String(length=30), nullable=False),
    sa.Column('teacher', sa.String(length=30), nullable=False),
    sa.Column('specialty', sa.String(length=50), nullable=False),
    sa.Column('semester', sa.Integer(), nullable=False),
    sa.Column('type_occupation', sa.Enum('Lecture', 'Practical', 'Laboratory', 'Seminar', name='subjecttype'), nullable=True),
    sa.Column('control', sa.Enum('Missing', 'Test', 'Examination', name='controltype'), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('subject')
    # ### end Alembic commands ###