"""Make user_id column non-nullable

Revision ID: b019b739ae86
Revises: 05c769296c74
Create Date: 2024-10-22 23:00:00

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.orm import Session
from myapp import User  # 必要に応じてインポートパスを調整

# revision identifiers, used by Alembic.
revision = 'b019b739ae86'
down_revision = '05c769296c74'
branch_labels = None
depends_on = None

def upgrade():
    # デフォルトユーザーを取得または作成
    bind = op.get_bind()
    session = Session(bind=bind)

    default_user = session.query(User).filter_by(username='default_user').first()
    if not default_user:
        default_user = User(username='default_user', password='hashed_password')  # パスワードは適切にハッシュ化してください
        session.add(default_user)
        session.commit()

    # 既存の投稿の user_id をデフォルトユーザーに設定
    session.execute(
        sa.text("UPDATE post SET user_id = :default_id WHERE user_id IS NULL"),
        {"default_id": default_user.id}
    )
    session.commit()

    # user_id カラムを nullable=False に変更
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.alter_column('user_id',
        existing_type=sa.Integer(),
        nullable=False)

    session.close()

def downgrade():
    # user_id カラムを nullable=True に戻す
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.alter_column('user_id',
        existing_type=sa.Integer(),
        nullable=True)
