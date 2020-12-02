import json
import traceback

import sqlalchemy as sa

from app.database import Session
from app.datatables import serve_datatable
from app.models import Collections, SetsCollections, Gene, Geneset, GenesetGene, Drug, Drugset, DrugsetDrug


def get_collection(id):
    try:
        sess = Session()
        r = {'sets': {'drugsets': [], 'genesets': []}}
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

        r['name'] = sess.query(Collections).filter(Collections.id == id).first().name
        r['description'] = sess.query(Collections).filter(Collections.id == id).first().description
        sess.close()
        r['sets']['drugsets'] = drugsets
        r['sets']['genesets'] = genesets
        return json.dumps(r, default=str), 200, {'ContentType': 'application/json'}
    except Exception as e:
        traceback.print_exc()
        return json.dumps({'error': str(e)}), 404, {'ContentType': 'application/json'}


serve_collection_drugset_datatable = lambda collection_id: serve_datatable(
    lambda sess, collection_id=collection_id: sess.query(Drugset).join(SetsCollections, Drugset.id == SetsCollections.set_id).filter(SetsCollections.type == 0).filter(SetsCollections.collection_id == collection_id),
    [
        (Drugset.id, 'id'),
        (Drugset.enrichrShortId, 'enrichrShortId'),
        (Drugset.enrichrUserListId, 'enrichrUserListId'),
        (Drugset.descrShort, 'descrShort'),
        (Drugset.descrFull, 'descrFull'),
        (Drugset.drugs, 'drugs'),
        (Drugset.authorName, 'authorName'),
        (Drugset.authorAffiliation, 'authorAffiliation'),
        (Drugset.authorEmail, 'authorEmail'),
        (Drugset.source, 'source'),
        (Drugset.date, 'date'),
        (Drugset.showContacts, 'showContacts'),
        (Drugset.meta, 'meta'),
        (Drugset.category, 'category'),
    ],
    lambda sess, s: sa.or_(
        Drugset.id.in_(
            sess.query(DrugsetDrug.drugset) \
                .join(Drug, Drug.id == DrugsetDrug.drug) \
                .filter(Drug.symbol.like(f'{s}%'))
        ),
        Drugset.descrShort.like(f'%{s}%'),
        Drugset.descrFull.like(f'%{s}%'),
        Drugset.source.like(f'%{s}%'),
        Drugset.meta.like(f'%{s}%'),
        Drugset.date.like(f'%{s}%'),
        sa.and_(
            Drugset.showContacts == 1,
            sa.or_(
                Drugset.authorName.like(f'%{s}%'),
                Drugset.authorAffiliation.like(f'%{s}%'),
                Drugset.authorEmail.like(f'%{s}%'),
            ),
        ),
    ),
    lambda qs: [
        {
            'id': record.id,
            'enrichrShortId': record.enrichrShortId,
            'enrichrUserListId': record.enrichrUserListId,
            'descrShort': record.descrShort,
            'descrFull': record.descrFull,
            'drugs': [gene.symbol for gene in record.drugs],
            'authorName': record.authorName if record.showContacts else '',
            'authorAffiliation': record.authorAffiliation if record.showContacts else '',
            'authorEmail': record.authorEmail if record.showContacts else '',
            'source': record.source,
            'date': record.date,
            'showContacts': record.showContacts,
            'meta': record.meta,
            'category': record.category,
        }
        for record in qs
    ]
)

serve_collection_drugset_filtered_datatable = lambda collection_id: serve_datatable(
    lambda sess, collection_id=collection_id: sess.query(Drugset).join(SetsCollections, Drugset.id == SetsCollections.set_id).filter(SetsCollections.type == 0).filter(SetsCollections.collection_id == collection_id),
    [
        (Drugset.id, 'id'),
        (Drugset.enrichrShortId, 'enrichrShortId'),
        (Drugset.enrichrUserListId, 'enrichrUserListId'),
        (Drugset.descrShort, 'descrShort'),
        (Drugset.descrFull, 'descrFull'),
        (Drugset.drugs, 'drugs'),
        (Drugset.authorName, 'authorName'),
        (Drugset.authorAffiliation, 'authorAffiliation'),
        (Drugset.authorEmail, 'authorEmail'),
        (Drugset.source, 'source'),
        (Drugset.date, 'date'),
        (Drugset.showContacts, 'showContacts'),
        (Drugset.meta, 'meta'),
        (Drugset.category, 'category'),
    ],
    lambda sess, s: sa.or_(
        Drugset.id.in_(
            sess.query(DrugsetDrug.drugset) \
                .join(Drug, Drug.id == DrugsetDrug.drug) \
                .filter(Drug.symbol.like(f'{s}%'))
        ),
        Drugset.descrShort.like(f'%{s}%'),
        Drugset.descrFull.like(f'%{s}%'),
        Drugset.source.like(f'%{s}%'),
        Drugset.meta.like(f'%{s}%'),
        Drugset.date.like(f'%{s}%'),
        sa.and_(
            Drugset.showContacts == 1,
            sa.or_(
                Drugset.authorName.like(f'%{s}%'),
                Drugset.authorAffiliation.like(f'%{s}%'),
                Drugset.authorEmail.like(f'%{s}%'),
            ),
        ),
    ),
    lambda qs: [
        {
            'id': record.id,
            'enrichrShortId': record.enrichrShortId,
            'enrichrUserListId': record.enrichrUserListId,
            'descrShort': record.descrShort,
            'descrFull': record.descrFull,
            'drugs': [gene.symbol for gene in record.drugs],
            'authorName': record.authorName if record.showContacts else '',
            'authorAffiliation': record.authorAffiliation if record.showContacts else '',
            'authorEmail': record.authorEmail if record.showContacts else '',
            'source': record.source,
            'date': record.date,
            'showContacts': record.showContacts,
            'meta': record.meta,
            'category': record.category,
        }
        for record in qs
    ]
)