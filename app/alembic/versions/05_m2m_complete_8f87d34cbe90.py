"""05 m2m complete

Revision ID: 8f87d34cbe90
Revises: 6b2e3f09c313
Create Date: 2020-04-01 18:32:11.798173

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '8f87d34cbe90'
down_revision = '6b2e3f09c313'
branch_labels = None
depends_on = None


def upgrade():
    if op.get_context().dialect.driver == 'pysqlite':
        with op.batch_alter_table('drugsets') as batch_op:
            batch_op.drop_column('drugs')
        
        with op.batch_alter_table('genesets') as batch_op:
            batch_op.drop_column('genes')
    else:
        op.drop_column('drugsets', 'drugs')
        op.drop_column('genesets', 'genes')


def downgrade():
    if op.get_context().dialect.driver == 'pysqlite':
        op.add_column('genesets', sa.Column('genes', sa.Text(), server_default='', nullable=False))
        op.add_column('drugsets', sa.Column('drugs', sa.Text(), server_default='', nullable=False))
    else:
        op.add_column('genesets', sa.Column('genes', sa.Text(), nullable=False))
        op.add_column('drugsets', sa.Column('drugs', sa.Text(), nullable=False))
