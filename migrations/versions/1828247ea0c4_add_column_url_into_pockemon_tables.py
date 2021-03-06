"""Add column url into pockemon tables

Revision ID: 1828247ea0c4
Revises: 7bbc914d8c1e
Create Date: 2021-02-16 11:47:41.861988

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1828247ea0c4'
down_revision = '7bbc914d8c1e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('pockemon', sa.Column('url', sa.String(length=1), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('pockemon', 'url')
    # ### end Alembic commands ###
