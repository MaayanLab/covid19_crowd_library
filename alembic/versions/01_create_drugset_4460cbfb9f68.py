"""01 create drugset

Revision ID: 4460cbfb9f68
Revises: 342a18cb2b70
Create Date: 2020-04-01 15:31:54.164388

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '4460cbfb9f68'
down_revision = '342a18cb2b70'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('drugsets',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('drugs', sa.Text(), nullable=False),
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
    op.drop_table('drugsets')
