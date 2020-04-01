"""05 m2m complete

Revision ID: 8f87d34cbe90
Revises: 6b2e3f09c313
Create Date: 2020-04-01 18:32:11.798173

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '8f87d34cbe90'
down_revision = '6b2e3f09c313'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_column('drugsets', 'drugs')
    op.drop_column('genesets', 'genes')


def downgrade():
    op.add_column('genesets', sa.Column('genes', mysql.TEXT(), nullable=False))
    op.add_column('drugsets', sa.Column('drugs', mysql.TEXT(), nullable=False))
