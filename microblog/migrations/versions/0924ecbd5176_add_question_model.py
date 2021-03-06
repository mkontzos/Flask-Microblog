"""add question model

Revision ID: 0924ecbd5176
Revises: 4a150967b373
Create Date: 2022-01-11 14:07:19.873468

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0924ecbd5176'
down_revision = '4a150967b373'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('question',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=64), nullable=True),
    sa.Column('body', sa.String(length=140), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_question_timestamp'), 'question', ['timestamp'], unique=False)
    op.create_index(op.f('ix_question_title'), 'question', ['title'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_question_title'), table_name='question')
    op.drop_index(op.f('ix_question_timestamp'), table_name='question')
    op.drop_table('question')
    # ### end Alembic commands ###
