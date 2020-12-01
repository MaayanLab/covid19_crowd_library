import json
import traceback
from itertools import combinations
import sqlalchemy as sa
from app.database import Session
from app.models import Collections, SetsCollections
from app.datatables import serve_datatable
from app.utils import match_meta, enrichr_submit


def get_collection(id):
    try:
        sess = Session()
        set_ids = sess.query(SetsCollections).filter(SetsCollections.collection_id == id).first().jsonify()
        r = [g.jsonify() for g in sess.query(Geneset).filter(Geneset.reviewed == reviewed)]
        sess.close()

        return json.dumps(r, default=str), 200, {'ContentType': 'application/json'}
    except Exception as e:
        traceback.print_exc()
        return json.dumps({'error': str(e)}), 404, {'ContentType': 'application/json'}
