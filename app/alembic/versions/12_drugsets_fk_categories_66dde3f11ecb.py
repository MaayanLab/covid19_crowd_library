"""Drugsets FK Categories

Revision ID: 66dde3f11ecb
Revises: 94ad0824ffb3
Create Date: 2020-04-29 17:03:32.939510

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

from app.database import Session
from app.alembic.models import models_11_94ad0824ffb3

# revision identifiers, used by Alembic.
revision = '66dde3f11ecb'
down_revision = '94ad0824ffb3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###

    # Add the default category 'all'
    sess = Session(bind=op.get_bind())
    sess.add(models_11_94ad0824ffb3.Categories())
    sess.commit()
    op.create_index('categories_name_uindex', 'categories', ['name'], unique=True)
    op.create_foreign_key('drugsets_categories_id_fk', 'drugsets', 'categories', ['category'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('drugsets_categories_id_fk', 'drugsets', type_='foreignkey')
    op.drop_index('categories_name_uindex', table_name='categories')
    # ### end Alembic commands ###
