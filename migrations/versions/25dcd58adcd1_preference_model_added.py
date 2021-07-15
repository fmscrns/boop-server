"""preference model added

Revision ID: 25dcd58adcd1
Revises: 15963c49bed9
Create Date: 2021-07-04 16:06:03.900954

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '25dcd58adcd1'
down_revision = '15963c49bed9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('preference',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('public_id', sa.String(length=100), nullable=False),
    sa.Column('user_selector_id', sa.String(), nullable=False),
    sa.Column('is_followed', sa.Boolean(), nullable=True),
    sa.Column('breed_subgroup_id', sa.String(), nullable=True),
    sa.Column('business_type_id', sa.String(), nullable=True),
    sa.Column('circle_type_id', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['breed_subgroup_id'], ['breed.public_id'], ),
    sa.ForeignKeyConstraint(['business_type_id'], ['business_type.public_id'], ),
    sa.ForeignKeyConstraint(['circle_type_id'], ['circle_type.public_id'], ),
    sa.ForeignKeyConstraint(['user_selector_id'], ['user.public_id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('public_id')
    )
    op.alter_column('user', 'admin',
               existing_type=sa.BOOLEAN(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'admin',
               existing_type=sa.BOOLEAN(),
               nullable=False)
    op.drop_table('preference')
    # ### end Alembic commands ###