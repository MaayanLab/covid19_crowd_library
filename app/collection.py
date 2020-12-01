import json
import traceback
from itertools import combinations
import sqlalchemy as sa
from app.database import Session
from app.models import SetsCollections, Drugset, Geneset
from app.datatables import serve_datatable


def get_collection(id):
    try:
        sess = Session()
        drugset_ids = sess.query(SetsCollections).filter(SetsCollections.collection_id == id).filter(SetsCollections.type == 0).first().jsonify()
        drugsets = [sess.query(Drugset).filter(Drugset.id == id)[0].jsonify() for id in drugset_ids]
        geneset_ids = sess.query(SetsCollections).filter(SetsCollections.collection_id == id).filter(SetsCollections.type == 1).first().jsonify()
        genesets = [sess.query(Geneset).filter(Geneset.id == id)[0].jsonify() for id in geneset_ids]

        sess.close()
        r = drugsets.append(genesets)
        return json.dumps(r, default=str), 200, {'ContentType': 'application/json'}
    except Exception as e:
        traceback.print_exc()
        return json.dumps({'error': str(e)}), 404, {'ContentType': 'application/json'}
