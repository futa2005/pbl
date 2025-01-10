"""Add PostLike model

Revision ID: bd8e97d09a07
Revises: b019b739ae86
Create Date: 2024-04-27 12:00:00.000000
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'bd8e97d09a07'
down_revision = 'b019b739ae86'
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'post_like',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('user.id'), nullable=False),
        sa.Column('post_id', sa.Integer(), sa.ForeignKey('post.id'), nullable=False),
        sa.Column('like_count', sa.Integer(), nullable=False, server_default='0'),
    )

def downgrade():
    op.drop_table('post_like')
