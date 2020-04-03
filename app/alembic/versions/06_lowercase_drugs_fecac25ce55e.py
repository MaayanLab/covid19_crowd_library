"""06 lowercase drugs

Revision ID: fecac25ce55e
Revises: 8f87d34cbe90
Create Date: 2020-04-03 16:40:11.079395

"""
from alembic import op
from collections import Counter
import sqlalchemy as sa

import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from app.database import Session
from app.alembic.models import models_05_8f87d34cbe90

# revision identifiers, used by Alembic.
revision = 'fecac25ce55e'
down_revision = '8f87d34cbe90'
branch_labels = None
depends_on = None


def upgrade():
    sess = Session(bind=op.get_bind())
    # Ensure all drugs have a lowercase instance
    lowercase_instances = {
        instance.symbol: instance
        for instance in models_05_8f87d34cbe90.Drug.resolve_set(
            sess,
            {
                symbol.lower()
                for (symbol,) in sess.query(models_05_8f87d34cbe90.Drug.symbol)
            }
        )
    }
    # Explicitly set it on the instance to be sure (mysql)
    for instance in lowercase_instances.values():
        instance.symbol = instance.symbol.lower()
    sess.commit()
    print(instance.symbol)
    # find all drugs that must be transfered
    drug_to_remove = []
    drugset_drug_to_remove = []
    drugset_drug_to_add = []
    for drug in sess.query(models_05_8f87d34cbe90.Drug).filter(
        models_05_8f87d34cbe90.Drug.id.notin_(tuple(v.id for v in lowercase_instances.values()))
    ):
        drug_to_remove.append(drug.id)
        for drugset in drug.drugsets:
            drugset_drug_to_remove.append(dict(drug=drug.id, drugset=drugset.id))
            drugset_drug_to_add.append(dict(drug=lowercase_instances[drug.symbol.lower()].id, drugset=drugset.id))
    # update m2m
    for item in drugset_drug_to_remove:
        sess.delete(sess.query(models_05_8f87d34cbe90.DrugsetDrug).get(item))
    for item in drugset_drug_to_add:
        sess.add(models_05_8f87d34cbe90.DrugsetDrug(**item))
    sess.commit()
    # update drugs
    for item in drug_to_remove:
        sess.delete(sess.query(models_05_8f87d34cbe90.Drug).get(item))
    sess.commit()

def downgrade():
    # this is a one-directional transformation
    pass
