"""03 m2m

Revision ID: 899a089268fa
Revises: dc18a84a5406
Create Date: 2020-04-01 17:22:08.967645

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '899a089268fa'
down_revision = 'dc18a84a5406'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('drugs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('symbol', sa.String(length=256), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('genes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('symbol', sa.String(length=32), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('drugsets_drugs',
    sa.Column('drugset', sa.Integer(), nullable=False),
    sa.Column('drug', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['drug'], ['drugs.id'], ),
    sa.ForeignKeyConstraint(['drugset'], ['drugsets.id'], ),
    sa.PrimaryKeyConstraint('drugset', 'drug')
    )
    op.create_table('genesets_genes',
    sa.Column('geneset', sa.Integer(), nullable=False),
    sa.Column('gene', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['gene'], ['genes.id'], ),
    sa.ForeignKeyConstraint(['geneset'], ['genesets.id'], ),
    sa.PrimaryKeyConstraint('geneset', 'gene')
    )


def downgrade():
    op.drop_table('genesets_genes')
    op.drop_table('drugsets_drugs')
    op.drop_table('genes')
    op.drop_table('drugs')
