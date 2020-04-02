"""04 m2m data transfer

Revision ID: 6b2e3f09c313
Revises: 899a089268fa
Create Date: 2020-04-01 17:23:37.749315

NOTE if this one fails, you should probably revert 03 as well.
"""
from alembic import op
import sqlalchemy as sa

import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from app.database import Session
from app.alembic.models import models_02_dc18a84a5406, models_03_899a089268fa

# revision identifiers, used by Alembic.
revision = '6b2e3f09c313'
down_revision = '899a089268fa'
branch_labels = None
depends_on = None


def upgrade():
    sess = Session(bind=op.get_bind())

    # Get all unique genes
    genes = set.union(set(), *[
        set(genes)
        for (genes,) in sess.query(models_02_dc18a84a5406.Geneset.genes)
    ])

    # Add genes
    for symbol in genes:
        sess.add(models_03_899a089268fa.Gene(symbol=symbol))
    sess.commit()

    # Construct a symbol lookup table for these genes
    gene_lookup = {
        gene.symbol: gene.id
        for gene in sess.query(models_03_899a089268fa.Gene)
    }

    # Add GenesetGene
    for geneset in sess.query(models_02_dc18a84a5406.Geneset):
        for gene_id in set(map(gene_lookup.get, geneset.genes)):
            sess.add(models_03_899a089268fa.GenesetGene(geneset=geneset.id, gene=gene_id))
    sess.commit()

    # Confirm equivalence
    for geneset_02, geneset_03 in zip(sess.query(models_02_dc18a84a5406.Geneset), sess.query(models_03_899a089268fa.Geneset)):
        assert geneset_02.jsonify() == geneset_03.jsonify(deep=True), '{} != {}'.format(
            str(geneset_02.jsonify()),
            str(geneset_03.jsonify(deep=True))
        )

    # Get all unique drugs
    drugs = set.union(set(), *[
        set(drugs)
        for (drugs,) in sess.query(models_02_dc18a84a5406.Drugset.drugs)
    ])

    # Add drugs
    for symbol in drugs:
        sess.add(models_03_899a089268fa.Drug(symbol=symbol))
    sess.commit()

    # Construct a symbol lookup table for these drugs
    drug_lookup = {
        drug.symbol: drug.id
        for drug in sess.query(models_03_899a089268fa.Drug)
    }

    # Add drugsetdrug
    for drugset in sess.query(models_02_dc18a84a5406.Drugset):
        for drug_id in set(map(drug_lookup.get, drugset.drugs)):
            sess.add(models_03_899a089268fa.DrugsetDrug(drugset=drugset.id, drug=drug_id))
    sess.commit()

    # Confirm equivalence
    for drugset_02, drugset_03 in zip(sess.query(models_02_dc18a84a5406.Drugset), sess.query(models_03_899a089268fa.Drugset)):
        assert drugset_02.jsonify() == drugset_03.jsonify(deep=True)

    sess.close()

def downgrade():
    sess = Session(bind=op.get_bind())

    gene_lookup = {
        gene.id: gene.symbol
        for gene in sess.query(models_03_899a089268fa.Gene)
    }
    for geneset in sess.query(models_02_dc18a84a5406.Geneset):
        geneset.genes = [
            gene_lookup[geneset_genes.gene]
            for geneset_genes in sess.query(models_03_899a089268fa.GenesetGene).filter(models_03_899a089268fa.GenesetGene.geneset == geneset.id)
        ]
    sess.commit()

    # Confirm equivalence
    for geneset_02, geneset_03 in zip(sess.query(models_02_dc18a84a5406.Geneset), sess.query(models_03_899a089268fa.Geneset)):
        assert geneset_02.jsonify() == geneset_03.jsonify(deep=True)

    drug_lookup = {
        drug.id: drug.symbol
        for drug in sess.query(models_03_899a089268fa.Drug)
    }
    for drugset in sess.query(models_02_dc18a84a5406.Drugset):
        drugset.drugs = [
            drug_lookup[drugset_drugs.drug]
            for drugset_drugs in sess.query(models_03_899a089268fa.DrugsetDrug).filter(models_03_899a089268fa.DrugsetDrug.drugset == drugset.id)
        ]
    sess.commit()

    # Confirm equivalence
    for drugset_02, drugset_03 in zip(sess.query(models_02_dc18a84a5406.Drugset), sess.query(models_03_899a089268fa.Drugset)):
        assert drugset_02.jsonify() == drugset_03.jsonify(deep=True)

    sess.close()
