"""empty message

Revision ID: dc3e4dd7d916
Revises: 197116b9ef66
Create Date: 2018-12-05 20:47:37.184167

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dc3e4dd7d916'
down_revision = '197116b9ef66'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('answer', sa.Column('creat_time', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('answer', 'creat_time')
    # ### end Alembic commands ###
