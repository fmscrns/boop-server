"""added 4 photo columns for post model

Revision ID: 1dc4f0791a1f
Revises: 080b3e9c8af0
Create Date: 2021-06-22 16:05:35.870007

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1dc4f0791a1f'
down_revision = '080b3e9c8af0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('post', sa.Column('photo_1', sa.String(length=50), nullable=True))
    op.add_column('post', sa.Column('photo_2', sa.String(length=50), nullable=True))
    op.add_column('post', sa.Column('photo_3', sa.String(length=50), nullable=True))
    op.add_column('post', sa.Column('photo_4', sa.String(length=50), nullable=True))
    op.drop_column('post', 'photo')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('post', sa.Column('photo', sa.VARCHAR(length=50), autoincrement=False, nullable=True))
    op.drop_column('post', 'photo_4')
    op.drop_column('post', 'photo_3')
    op.drop_column('post', 'photo_2')
    op.drop_column('post', 'photo_1')
    # ### end Alembic commands ###