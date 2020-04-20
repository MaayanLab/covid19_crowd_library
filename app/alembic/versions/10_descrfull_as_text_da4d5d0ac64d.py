"""descrFull as text

Revision ID: da4d5d0ac64d
Revises: ebd6a61d7c83
Create Date: 2020-04-20 19:14:32.045189

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'da4d5d0ac64d'
down_revision = 'ebd6a61d7c83'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column(
        table_name='genesets',
        column_name='descrFull',
        nullable=False,
        type_=sa.Text()
    )
    op.alter_column(
        table_name='drugsets',
        column_name='descrFull',
        nullable=False,
        type_=sa.Text()
    )


def downgrade():
    # Depending on size of values in descrFull, this may or may not work
    op.alter_column(
        table_name='genesets',
        column_name='descrFull',
        nullable=False,
        type_=sa.String(255)
    )
    op.alter_column(
        table_name='drugsets',
        column_name='descrFull',
        nullable=False,
        type_=sa.String(255)
    )
