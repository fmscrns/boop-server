"""empty message

Revision ID: 0406c9db66b2
Revises: 71d69b274c4e
Create Date: 2021-05-19 18:31:11.432214

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '0406c9db66b2'
down_revision = '71d69b274c4e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('circle_member_table',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('public_id', sa.String(length=100), nullable=True),
    sa.Column('circle_pid', sa.String(length=100), nullable=True),
    sa.Column('member_pid', sa.String(length=100), nullable=True),
    sa.Column('is_accepted', sa.Boolean(), nullable=True),
    sa.Column('is_admin', sa.Boolean(), nullable=True),
    sa.Column('registered_on', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['circle_pid'], ['circle.public_id'], ),
    sa.ForeignKeyConstraint(['member_pid'], ['user.public_id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('public_id')
    )
    op.drop_table('circle_membership_table')
    op.drop_constraint('circle_user_admin_id_fkey', 'circle', type_='foreignkey')
    op.drop_column('circle', 'user_admin_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('circle', sa.Column('user_admin_id', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.create_foreign_key('circle_user_admin_id_fkey', 'circle', 'user', ['user_admin_id'], ['public_id'])
    op.create_table('circle_membership_table',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('public_id', sa.VARCHAR(length=100), autoincrement=False, nullable=True),
    sa.Column('circle_pid', sa.VARCHAR(length=100), autoincrement=False, nullable=True),
    sa.Column('member_pid', sa.VARCHAR(length=100), autoincrement=False, nullable=True),
    sa.Column('registered_on', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['circle_pid'], ['circle.public_id'], name='circle_membership_table_circle_pid_fkey'),
    sa.ForeignKeyConstraint(['member_pid'], ['user.public_id'], name='circle_membership_table_member_pid_fkey'),
    sa.PrimaryKeyConstraint('id', name='circle_membership_table_pkey'),
    sa.UniqueConstraint('public_id', name='circle_membership_table_public_id_key')
    )
    op.drop_table('circle_member_table')
    # ### end Alembic commands ###