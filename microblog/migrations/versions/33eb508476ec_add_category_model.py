"""add category model

Revision ID: 33eb508476ec
Revises: c9b46b45d6e1
Create Date: 2022-01-11 14:29:59.233815

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '33eb508476ec'
down_revision = 'c9b46b45d6e1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('category',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=40), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('question', sa.Column('category', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'question', 'category', ['category'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'question', type_='foreignkey')
    op.drop_column('question', 'category')
    op.drop_table('category')
    # ### end Alembic commands ###
