from app.database import Session
from app.models import Geneset, Drugset

def genesets():
  sess = Session()
  for geneset in sess.query(Geneset):
    yield geneset.to_gmt() + '\n'
  sess.close()

def drugsets():
  sess = Session()
  for drugset in sess.query(Drugset):
    yield drugset.to_gmt() + '\n'
  sess.close()
