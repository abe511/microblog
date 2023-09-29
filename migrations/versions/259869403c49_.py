"""empty message

Revision ID: 259869403c49
Revises: a3084c3f2acf
Create Date: 2023-09-29 09:26:53.555324

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '259869403c49'
down_revision = 'a3084c3f2acf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('read', sa.Boolean(), nullable=True))
        batch_op.add_column(sa.Column('write', sa.Boolean(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('write')
        batch_op.drop_column('read')

    # ### end Alembic commands ###
