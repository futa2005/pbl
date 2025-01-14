"""Add likes column to Post

Revision ID: 803c1e156452
Revises: 7ac35931f6a0
Create Date: 2024-10-22 09:57:03.302000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '803c1e156452'
down_revision = '7ac35931f6a0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.add_column(sa.Column('likes', sa.Integer(), server_default=sa.text('0'), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.drop_column('likes')

    # ### end Alembic commands ###
