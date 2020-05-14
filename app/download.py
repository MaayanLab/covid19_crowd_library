from app.database import Session
from app.models import Geneset, Drugset


def genesets():
    sess = Session()
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
