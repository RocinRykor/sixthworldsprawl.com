"""remove user email

Revision ID: 65c09560a30c
Revises: 93be00ae91df
Create Date: 2022-12-09 18:41:39.008781

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '65c09560a30c'
down_revision = '93be00ae91df'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'email')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('email', mysql.VARCHAR(length=256), nullable=False))
    # ### end Alembic commands ###
