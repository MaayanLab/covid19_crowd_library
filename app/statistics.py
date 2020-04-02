import sqlalchemy as sa
from app.database import Session
from app.models import Geneset, GenesetGene, Gene, Drugset, DrugsetDrug, Drug

def top_genes(offset=0, limit=100):
  sess = Session()
  gene_count = sa.func.count(Gene.id)
  qs = sess.query(Gene.symbol, gene_count) \
    .join(GenesetGene, GenesetGene.gene == Gene.id) \
    .join(Geneset, GenesetGene.geneset == Geneset.id) \
    .group_by(Gene.id) \
    .order_by(gene_count.desc()) \
    .offset(offset) \
    .limit(limit)
  for gene, count in qs:
    yield dict(symbol=gene, count=count)
  sess.close()

def top_drugs(offset=0, limit=100):
  sess = Session()
  drug_count = sa.func.count(Drug.id)
  qs = sess.query(Drug.symbol, drug_count) \
    .join(DrugsetDrug, DrugsetDrug.drug == Drug.id) \
    .join(Drugset, DrugsetDrug.drugset == Drugset.id) \
    .group_by(Drug.id) \
    .order_by(drug_count.desc()) \
    .offset(offset) \
    .limit(limit)
  for drug, count in qs:
    yield dict(symbol=drug, count=count)
  sess.close()
