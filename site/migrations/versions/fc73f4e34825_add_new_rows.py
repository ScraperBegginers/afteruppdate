"""add new rows

Revision ID: fc73f4e34825
Revises: 
Create Date: 2024-12-16 22:01:22.735976

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fc73f4e34825'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('tasks', schema=None) as batch_op:
        batch_op.add_column(sa.Column('channel_id', sa.String(length=80), nullable=True))
        batch_op.alter_column('link',
               existing_type=sa.VARCHAR(length=80),
               nullable=True)

    with op.batch_alter_table('tasks_completed', schema=None) as batch_op:
        batch_op.add_column(sa.Column('channel_id', sa.String(length=80), nullable=False))
        batch_op.drop_column('link')

    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('get_bonus_for_two_friends',
               existing_type=sa.BOOLEAN(),
               type_=sa.String(length=2),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('get_bonus_for_two_friends',
               existing_type=sa.String(length=2),
               type_=sa.BOOLEAN(),
               existing_nullable=False)

    with op.batch_alter_table('tasks_completed', schema=None) as batch_op:
        batch_op.add_column(sa.Column('link', sa.VARCHAR(length=80), nullable=False))
        batch_op.drop_column('channel_id')

    with op.batch_alter_table('tasks', schema=None) as batch_op:
        batch_op.alter_column('link',
               existing_type=sa.VARCHAR(length=80),
               nullable=False)
        batch_op.drop_column('channel_id')

    # ### end Alembic commands ###