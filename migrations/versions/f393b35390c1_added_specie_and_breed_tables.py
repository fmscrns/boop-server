"""added specie and breed tables

Revision ID: f393b35390c1
Revises: e6d8f6527388
Create Date: 2020-12-08 21:41:47.882699

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f393b35390c1'
down_revision = 'e6d8f6527388'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('specie',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('public_id', sa.String(length=100), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('registered_on', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name'),
    sa.UniqueConstraint('public_id')
    )
    op.create_table('breed',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('public_id', sa.String(length=100), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('registered_on', sa.DateTime(), nullable=False),
    sa.Column('specie_parent_id', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['specie_parent_id'], ['specie.public_id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name'),
    sa.UniqueConstraint('public_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('breed')
    op.drop_table('specie')
    # ### end Alembic commands ###