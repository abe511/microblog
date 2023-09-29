"""empty message

Revision ID: 3bd41a083f59
Revises: 411ff537cb54
Create Date: 2023-09-29 03:16:26.070916

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3bd41a083f59'
down_revision = '411ff537cb54'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users_groups_association_table',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('group_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['group_id'], ['group.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], )
    )
    with op.batch_alter_table('group', schema=None) as batch_op:
        batch_op.add_column(sa.Column('created', sa.DateTime(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('group', schema=None) as batch_op:
        batch_op.drop_column('created')

    op.drop_table('users_groups_association_table')
    # ### end Alembic commands ###
