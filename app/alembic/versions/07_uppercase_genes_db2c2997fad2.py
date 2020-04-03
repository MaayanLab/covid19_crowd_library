"""07 uppercase genes

Revision ID: db2c2997fad2
Revises: fecac25ce55e
Create Date: 2020-04-03 17:22:40.469116

"""
from alembic import op
import sqlalchemy as sa

import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from app.database import Session
from app.alembic.models import models_05_8f87d34cbe90

# revision identifiers, used by Alembic.
revision = 'db2c2997fad2'
down_revision = 'fecac25ce55e'
branch_labels = None
depends_on = None


def upgrade():
    sess = Session(bind=op.get_bind())
    # Ensure all genes have a uppercase instance
    uppercase_instances = {
        instance.symbol: instance
        for instance in models_05_8f87d34cbe90.Gene.resolve_set(
            sess,
            {
                symbol.upper()
                for (symbol,) in sess.query(models_05_8f87d34cbe90.Gene.symbol)
            }
        )
    }
    # Explicitly set it on the instance to be sure (mysql)
    for instance in uppercase_instances.values():
        instance.symbol = instance.symbol.upper()
    sess.commit()
    # find all genes that must be transfered
    gene_to_remove = []
    geneset_genes_to_remove = []
    geneset_genes_to_add = []
    for gene in sess.query(models_05_8f87d34cbe90.Gene).filter(
        models_05_8f87d34cbe90.Gene.id.notin_(tuple(v.id for v in uppercase_instances.values()))
    ):
        gene_to_remove.append(gene.id)
        for geneset in gene.genesets:
            geneset_genes_to_remove.append(dict(gene=gene.id, geneset=geneset.id))
            geneset_genes_to_add.append(dict(gene=uppercase_instances[gene.symbol.upper()].id, geneset=geneset.id))
            
    # update m2m
    for item in geneset_genes_to_remove:
        sess.delete(sess.query(models_05_8f87d34cbe90.GenesetGene).get(item))
    for item in geneset_genes_to_add:
        sess.add(models_05_8f87d34cbe90.GenesetGene(**item))
    sess.commit()
    # update genes
    for item in gene_to_remove:
        sess.delete(sess.query(models_05_8f87d34cbe90.Gene).get(item))
    sess.commit()

def downgrade():
    # this is a one-directional transformation
    pass
