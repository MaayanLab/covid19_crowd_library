from app.database import Session
from app.models import Geneset, Drugset

def genesets():
  sess = Session()
  for geneset in sess.query(Geneset).filter(Geneset.reviewed == 1):
    yield geneset.to_gmt() + '\n'
  sess.close()

def drugsets():
  sess = Session()
  for drugset in sess.query(Drugset).filter(Drugset.reviewed == 1):
    yield drugset.to_gmt() + '\n'
  sess.close()
