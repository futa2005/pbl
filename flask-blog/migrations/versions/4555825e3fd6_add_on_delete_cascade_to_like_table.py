"""Add ON DELETE CASCADE to Like table

Revision ID: 4555825e3fd6
Revises: 00e1ee499de7
Create Date: 2024-12-20 11:53:53.986511

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4555825e3fd6'
down_revision = '00e1ee499de7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('like', schema=None) as batch_op:
        batch_op.drop_constraint('like_post_id_fkey', type_='foreignkey')
        batch_op.create_foreign_key(None, 'post', ['post_id'], ['id'], ondelete='CASCADE')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('like', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('like_post_id_fkey', 'post', ['post_id'], ['id'])

    # ### end Alembic commands ###
