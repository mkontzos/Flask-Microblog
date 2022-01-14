"""question language column

Revision ID: ffbc5ce5aa2f
Revises: 33eb508476ec
Create Date: 2022-01-13 11:13:33.915523

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ffbc5ce5aa2f'
down_revision = '33eb508476ec'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('answer', sa.Column('language', sa.String(length=5), nullable=True))
    op.add_column('category', sa.Column('language', sa.String(length=5), nullable=True))
    op.add_column('question', sa.Column('language', sa.String(length=5), nullable=True))
    op.create_foreign_key(None, 'question', 'category', ['category'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'question', type_='foreignkey')
    op.drop_column('question', 'language')
    op.drop_column('category', 'language')
    op.drop_column('answer', 'language')
    # ### end Alembic commands ###