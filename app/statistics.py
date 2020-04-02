import sqlalchemy as sa
from app.database import Session
from app.models import Geneset, GenesetGene, Gene, Drugset, DrugsetDrug, Drug
from app.datatables import serve_datatable

def stats():
  sess = Session()
  ret = {
    'n_genesets': sess.query(Geneset).count(),
    'n_drugsets': sess.query(Drugset).count(),
    'n_unique_genes': sess.query(Gene).count(),
    'n_unique_drugs': sess.query(Drug).count(),
  }
  sess.close()
  return ret


gene_count = sa.func.count(Gene.id)
def top_genes_qs(sess):
  return sess.query(Gene.symbol, gene_count) \
    .join(GenesetGene, GenesetGene.gene == Gene.id) \
    .join(Geneset, GenesetGene.geneset == Geneset.id) \
    .group_by(Gene.id)
def top_genes_search(val):
  return Gene.symbol.like(f'%{val}%')
top_genes = serve_datatable(top_genes_qs, [(Gene.symbol, 'symbol'), (gene_count, 'count')], top_genes_search)


drug_count = sa.func.count(Drug.id)
def top_drugs_qs(sess):
  return sess.query(Drug.symbol, drug_count) \
    .join(DrugsetDrug, DrugsetDrug.drug == Drug.id) \
    .join(Drugset, DrugsetDrug.drugset == Drugset.id) \
    .group_by(Drug.id)
def top_drugs_search(val):
  return Drug.symbol.like(f'%{val}%')
top_drugs = serve_datatable(top_drugs_qs, [(Drug.symbol, 'symbol'), (drug_count, 'count')], top_drugs_search)
