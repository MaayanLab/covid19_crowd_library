"""09 fix json meta artifacts

Revision ID: ebd6a61d7c83
Revises: 2a9652d72819
Create Date: 2020-04-10 14:33:10.362088

"""
from alembic import op
import json
import sqlalchemy as sa

import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from app.database import Session
from app.alembic.models import models_08_2a9652d72819

# revision identifiers, used by Alembic.
revision = 'ebd6a61d7c83'
down_revision = '2a9652d72819'
branch_labels = None
depends_on = None


def upgrade():
    sess = Session(bind=op.get_bind())
    for geneset in sess.query(models_08_2a9652d72819.Geneset):
        if type(geneset.meta) == str:
            geneset.meta = json.loads(geneset.meta)
    #
    for drugset in sess.query(models_08_2a9652d72819.Drugset):
        if type(drugset.meta) == str:
            drugset.meta = json.loads(drugset.meta)
    #
    sess.commit()

def downgrade():
    # this is a one-directional transformation
    pass
