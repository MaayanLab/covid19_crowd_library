from app.database import Session
from app.models import Geneset, Drugset

# TODO add dowlnoads for collections


def genesets(category=0):
    sess = Session()
    if category:
        for geneset in sess.query(Geneset).filter(Geneset.reviewed == 1).filter(Geneset.category == category):
            yield geneset.to_gmt() + '\n'
    else:
        for geneset in sess.query(Geneset).filter(Geneset.reviewed == 1):
            yield geneset.to_gmt() + '\n'

    sess.close()


def drugsets(category=0):
    sess = Session()
    if category:
        for drugset in sess.query(Drugset).filter(Drugset.reviewed == 1).filter(Drugset.category == category):
            yield drugset.to_gmt() + '\n'
    else:
        for drugset in sess.query(Drugset).filter(Drugset.reviewed == 1):
            yield drugset.to_gmt() + '\n'

    sess.close()
