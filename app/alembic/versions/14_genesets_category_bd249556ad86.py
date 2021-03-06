"""Genesets category

Revision ID: bd249556ad86
Revises: 0182cee73887
Create Date: 2020-10-26 18:51:36.026559

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'bd249556ad86'
down_revision = '0182cee73887'
branch_labels = None
depends_on = None

def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('genesets', sa.Column('category', mysql.INTEGER(display_width=11), server_default=sa.text('1'), autoincrement=False, nullable=True))
    op.create_foreign_key('genesets_categories_id_fk', 'genesets', 'categories', ['category'], ['id'])
    op.alter_column('drugsets', 'enrichrUserListId',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=True,
               existing_server_default=sa.text('0'))
    op.alter_column('drugsets', 'enrichrShortId',
               existing_type=mysql.VARCHAR(length=255),
               nullable=True)
    op.create_index('categories_name_uindex', 'categories', ['name'], unique=True)
    op.alter_column('categories', 'name',
               existing_type=mysql.VARCHAR(length=255),
               nullable=True,
               existing_server_default=sa.text("'all'"))
    # ### end Alembic commands ###
    

def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('categories', 'name',
               existing_type=mysql.VARCHAR(length=255),
               nullable=False,
               existing_server_default=sa.text("'all'"))
    op.drop_index('categories_name_uindex', table_name='categories')
    op.alter_column('drugsets', 'enrichrShortId',
               existing_type=mysql.VARCHAR(length=255),
               nullable=False)
    op.alter_column('drugsets', 'enrichrUserListId',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=False,
               existing_server_default=sa.text('0'))
    op.drop_constraint('genesets_categories_id_fk', 'genesets', type_='foreignkey')
    op.drop_column('genesets', 'category')
    # ### end Alembic commands ###
