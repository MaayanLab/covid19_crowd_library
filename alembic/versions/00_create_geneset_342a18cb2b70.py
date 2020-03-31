"""Create geneset

Revision ID: 342a18cb2b70
Revises: 
Create Date: 2020-03-30 14:06:50.647209

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '342a18cb2b70'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('genesets',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('enrichrShortId', sa.String(length=255), nullable=False),
        sa.Column('enrichrUserListId', sa.Integer(), nullable=False),
        sa.Column('genes', sa.Text(), nullable=False),
        sa.Column('descrShort', sa.String(length=255), nullable=False),
        sa.Column('descrFull', sa.String(length=255), nullable=False),
        sa.Column('authorName', sa.String(length=255), nullable=False),
        sa.Column('authorAffiliation', sa.String(length=255), nullable=True),
        sa.Column('authorEmail', sa.String(length=255), nullable=True),
        sa.Column('showContacts', sa.Integer(), nullable=False),
        sa.Column('reviewed', sa.Integer(), nullable=False),
        sa.Column('source', mysql.VARCHAR(length=255), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    pass# op.drop_table('genesets')
