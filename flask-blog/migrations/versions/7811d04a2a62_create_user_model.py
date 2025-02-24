"""Create User Model

Revision ID: 7811d04a2a62
Revises: 4a68d3b98948
Create Date: 2024-10-04 14:10:28.769714

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7811d04a2a62'
down_revision = '4a68d3b98948'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=30), nullable=False),
    sa.Column('password', sa.String(length=120), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    # ### end Alembic commands ###
