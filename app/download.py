import flask
from app.database import Session
from app.models import Geneset, Drugset

def genesets():
  def geneset_generator():
    sess = Session()
    for geneset in sess.query(Geneset).filter(Geneset.reviewed == 1):
      yield geneset.to_gmt() + '\n'
    sess.close()
  return flask.Response(geneset_generator(), mimetype='text/gmt')

def drugsets():
  def drugset_generator():
    sess = Session()
    for drugset in sess.query(Drugset).filter(Drugset.reviewed == 1):
      yield drugset.to_gmt() + '\n'
    sess.close()
  return flask.Response(drugset_generator(), mimetype='text/gmt')
