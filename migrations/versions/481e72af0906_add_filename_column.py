"""add filename column

Revision ID: 481e72af0906
Revises: 
Create Date: 2022-12-23 16:10:55.897526

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '481e72af0906'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('character', sa.Column('portrait_filename', sa.String(length=64), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('character', 'portrait_filename')
    # ### end Alembic commands ###