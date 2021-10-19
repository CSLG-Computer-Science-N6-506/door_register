"""empty message

Revision ID: b1ba5369842e
Revises: 65fffced34fe
Create Date: 2021-04-06 11:17:50.764786

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b1ba5369842e'
down_revision = '65fffced34fe'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('member',
    sa.Column('create_time', sa.DateTime(), nullable=True, comment='创建时间'),
    sa.Column('update_time', sa.DateTime(), nullable=True, comment='更新时间'),
    sa.Column('is_delete', sa.Integer(), nullable=True, comment='逻辑删除:0=未删除,1=删除'),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=30), nullable=True),
    sa.Column('card_id', sa.String(length=30), nullable=True),
    sa.Column('finger_id', sa.String(length=20), nullable=True),
    sa.Column('phone', sa.String(length=30), nullable=True),
    sa.Column('finger_data', sa.String(length=3072), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_member_card_id'), 'member', ['card_id'], unique=False)
    op.create_index(op.f('ix_member_finger_data'), 'member', ['finger_data'], unique=False)
    op.create_index(op.f('ix_member_finger_id'), 'member', ['finger_id'], unique=False)
    op.create_index(op.f('ix_member_id'), 'member', ['id'], unique=False)
    op.create_index(op.f('ix_member_name'), 'member', ['name'], unique=False)
    op.create_index(op.f('ix_member_phone'), 'member', ['phone'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_member_phone'), table_name='member')
    op.drop_index(op.f('ix_member_name'), table_name='member')
    op.drop_index(op.f('ix_member_id'), table_name='member')
    op.drop_index(op.f('ix_member_finger_id'), table_name='member')
    op.drop_index(op.f('ix_member_finger_data'), table_name='member')
    op.drop_index(op.f('ix_member_card_id'), table_name='member')
    op.drop_table('member')
    # ### end Alembic commands ###
