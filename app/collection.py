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
        r = []
        drugsets = []
        dsids_q = sess.query(SetsCollections).filter(SetsCollections.collection_id == id).filter(
            SetsCollections.type == 0)
        drugset_ids = [ds.set_id for ds in dsids_q if dsids_q.first() != None]
        if drugset_ids:
            drugsets = [sess.query(Drugset).filter(Drugset.id == drugset_id).first().jsonify() for drugset_id in drugset_ids]
        genesets = []
        gsids_q = sess.query(SetsCollections).filter(SetsCollections.collection_id == id).filter(
            SetsCollections.type == 1)
        geneset_ids = [gs.set_id for gs in gsids_q if gsids_q.first() != None]
        if geneset_ids:
            genesets = [sess.query(Geneset).filter(Geneset.id == geneset_id).first().jsonify() for geneset_id in geneset_ids]

        sess.close()
        r.extend(drugsets)
        r.extend(genesets)
        return json.dumps(r, default=str), 200, {'ContentType': 'application/json'}
    except Exception as e:
        traceback.print_exc()
        return json.dumps({'error': str(e)}), 404, {'ContentType': 'application/json'}
