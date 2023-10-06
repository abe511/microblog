"""empty message

Revision ID: 199219fa6d23
Revises: bb54b9bce8ed
Create Date: 2023-10-04 17:00:09.287255

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '199219fa6d23'
down_revision = 'bb54b9bce8ed'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.drop_column('updated')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.add_column(sa.Column('updated', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))

    # ### end Alembic commands ###