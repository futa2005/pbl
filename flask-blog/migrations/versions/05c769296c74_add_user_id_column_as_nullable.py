"""Add user_id column as nullable

Revision ID: 05c769296c74
Revises: 803c1e156452
Create Date: 2024-10-22 22:22:18.570625

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '05c769296c74'
down_revision = '803c1e156452'  # 直前のリビジョンIDに置き換えてください
branch_labels = None
depends_on = None

def upgrade():
    # user_id カラムを nullable=True で追加
    op.add_column('post', sa.Column('user_id', sa.Integer(), nullable=True))
    op.create_foreign_key('fk_post_user', 'post', 'user', ['user_id'], ['id'])

def downgrade():
    op.drop_constraint('fk_post_user', 'post', type_='foreignkey')
    op.drop_column('post', 'user_id')
