import sqlalchemy as sa
from app.database import Session
from app.models import Geneset, GenesetGene, Gene, Drugset, DrugsetDrug, Drug
from app.datatables import serve_datatable

gene_count = sa.func.count(Gene.id)
drug_count = sa.func.count(Drug.id)


def stats():
    sess = Session()
    ret = {
        'n_genesets': sess.query(Geneset).filter(Geneset.reviewed == 1).count(),
        'n_drugsets': sess.query(Drugset).filter(Drugset.reviewed == 1).count(),
        'n_unique_genes': sess.query(Gene).distinct(Gene.id) \
            .join(GenesetGene, GenesetGene.gene == Gene.id) \
            .join(Geneset, GenesetGene.geneset == Geneset.id) \
            .filter(Geneset.reviewed == 1) \
            .count(),
        'n_unique_drugs': sess.query(Drug).distinct(Drug.id) \
            .join(DrugsetDrug, DrugsetDrug.drug == Drug.id) \
            .join(Drugset, DrugsetDrug.drugset == Drugset.id) \
            .filter(Drugset.reviewed == 1) \
            .count(),
    }
    sess.close()
    return ret


def bar_drugs(categories=0):
    sess = Session()
    qs = {'2': top_drugs_exp, '3': top_drugs_comp, '4': top_drugs_tw}
    if categories:
        td = qs[categories](sess)
    else:
        td = top_drugs_qs(sess)
    sess.close()
    return [{'symbol': t[0], 'count': t[1]} for t in td]


def bar_genes():
    sess = Session()
    tg = top_genes_qs(sess)
    sess.close()
    return [{'symbol': t[0], 'count': t[1]} for t in tg]


def top_genes_qs(sess):
    return sess.query(Gene.symbol, gene_count) \
        .join(GenesetGene, GenesetGene.gene == Gene.id) \
        .join(Geneset, GenesetGene.geneset == Geneset.id) \
        .filter(Geneset.reviewed == 1) \
        .group_by(Gene.id)


def top_genes_search(sess, val):
    return Gene.symbol.like(f'%{val}%')


top_genes = serve_datatable(top_genes_qs, [(Gene.symbol, 'symbol'), (gene_count, 'count')], top_genes_search)


def top_drugs_qs(sess):
    return sess.query(Drug.symbol, drug_count) \
        .join(DrugsetDrug, DrugsetDrug.drug == Drug.id) \
        .join(Drugset, DrugsetDrug.drugset == Drugset.id) \
        .filter(Drugset.reviewed == 1) \
        .group_by(Drug.id)


def top_drugs_exp(sess):
    return sess.query(Drug.symbol, drug_count) \
        .join(DrugsetDrug, DrugsetDrug.drug == Drug.id) \
        .join(Drugset, DrugsetDrug.drugset == Drugset.id) \
        .filter(Drugset.reviewed == 1) \
        .filter(Drugset.category == 2) \
        .group_by(Drug.id)


def top_drugs_comp(sess):
    return sess.query(Drug.symbol, drug_count) \
        .join(DrugsetDrug, DrugsetDrug.drug == Drug.id) \
        .join(Drugset, DrugsetDrug.drugset == Drugset.id) \
        .filter(Drugset.reviewed == 1) \
        .filter(Drugset.category == 3) \
        .group_by(Drug.id)


def top_drugs_tw(sess):
    return sess.query(Drug.symbol, drug_count) \
        .join(DrugsetDrug, DrugsetDrug.drug == Drug.id) \
        .join(Drugset, DrugsetDrug.drugset == Drugset.id) \
        .filter(Drugset.reviewed == 1) \
        .filter(Drugset.category == 4) \
        .group_by(Drug.id)


def top_drugs_search(sess, val):
    return Drug.symbol.like(f'%{val}%')


top_drugs = serve_datatable(top_drugs_qs, [(Drug.symbol, 'symbol'), (drug_count, 'count')], top_drugs_search)


def top_drugs_categories(category, post):
    qs = {'2': top_drugs_exp, '3': top_drugs_comp, '4': top_drugs_tw}
    return serve_datatable(qs[category], [(Drug.symbol, 'symbol'), (drug_count, 'count')], top_drugs_search)(**post)


def genesets_submissions():
    sess = Session()
    q = sess.query(sa.cast(Geneset.date, sa.Date).label('date'), sa.func.count(sa.cast(Geneset.date, sa.Date)).label('count')).group_by(sa.cast(Geneset.date, sa.Date)).filter(Geneset.reviewed == 1)
    sess.close()
    return list(map(lambda x: {'date': str(x), 'count': dict(q)[x]}, dict(q)))


def drugsets_submissions():
    sess = Session()
    q = sess.query(sa.cast(Drugset.date, sa.Date).label('date'), sa.func.count(sa.cast(Drugset.date, sa.Date)).label('count')).group_by(sa.cast(Drugset.date, sa.Date)).filter(Drugset.reviewed == 1)
    sess.close()
    return list(map(lambda x: {'date': str(x), 'count': dict(q)[x]}, dict(q)))