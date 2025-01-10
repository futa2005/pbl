"""Merge multiple heads

Revision ID: 7b7934280e87
Revises: 8f11cb9e8320, bd8e97d09a07
Create Date: 2024-12-06 16:26:49.865149

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7b7934280e87'
down_revision = ('8f11cb9e8320', 'bd8e97d09a07')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
