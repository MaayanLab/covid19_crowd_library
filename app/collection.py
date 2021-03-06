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

        r['sets']['drugsets'] = [ds.jsonify() for ds in
                    sess.query(Drugset).join(SetsCollections, Drugset.id == SetsCollections.set_id).filter(
                        SetsCollections.type == 0).filter(SetsCollections.collection_id == id)]
        r['sets']['genesets'] = [gs.jsonify() for gs in
                    sess.query(Geneset).join(SetsCollections, Geneset.id == SetsCollections.set_id).filter(
                        SetsCollections.type == 1).filter(SetsCollections.collection_id == id)]
        r['name'] = sess.query(Collections).filter(Collections.id == id).first().name
        r['description'] = sess.query(Collections).filter(Collections.id == id).first().description
        r['id'] = id
        sess.close()
        return json.dumps(r, default=str), 200, {'ContentType': 'application/json'}
    except Exception as e:
        traceback.print_exc()
        return json.dumps({'error': str(e)}), 404, {'ContentType': 'application/json'}


def get_collections_sizes():
    # It's a draft/idae. It doesn't work
    sess = Session()
    collections = sess.query(Collections)
    for collection in collections:
        coll_size = sess.query(SetsCollections).filter(SetsCollections.collection_id == collection.id)
    return None

serve_collection_drugset_datatable = lambda collection_id: serve_datatable(
    lambda sess, collection_id=collection_id: sess.query(Drugset).filter(SetsCollections.type == 0).filter(SetsCollections.collection_id == collection_id).join(SetsCollections, Drugset.id == SetsCollections.set_id),
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
    lambda sess, collection_id=collection_id: sess.query(Drugset).filter(SetsCollections.type == 0).filter(SetsCollections.collection_id == collection_id).join(SetsCollections, Drugset.id == SetsCollections.set_id),
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

serve_collection_geneset_datatable = lambda collection_id: serve_datatable(
    lambda sess, collection_id=collection_id: sess.query(Geneset).filter(SetsCollections.type == 1).filter(SetsCollections.collection_id == collection_id).join(SetsCollections, Geneset.id == SetsCollections.set_id),
    [
        (Geneset.id, 'id'),
        (Geneset.enrichrShortId, 'enrichrShortId'),
        (Geneset.enrichrUserListId, 'enrichrUserListId'),
        (Geneset.descrShort, 'descrShort'),
        (Geneset.descrFull, 'descrFull'),
        (Geneset.genes, 'genes'),
        (Geneset.authorName, 'authorName'),
        (Geneset.authorAffiliation, 'authorAffiliation'),
        (Geneset.authorEmail, 'authorEmail'),
        (Geneset.source, 'source'),
        (Geneset.date, 'date'),
        (Geneset.showContacts, 'showContacts'),
        (Geneset.meta, 'meta'),
        (Geneset.category, 'category'),
    ],
    lambda sess, s: sa.or_(
        Geneset.id.in_(
            sess.query(GenesetGene.geneset) \
                .join(Gene, Gene.id == GenesetGene.gene) \
                .filter(Gene.symbol.like(f'{s}%'))
        ),
        Geneset.descrShort.like(f'%{s}%'),
        Geneset.descrFull.like(f'%{s}%'),
        Geneset.source.like(f'%{s}%'),
        Geneset.meta.like(f'%{s}%'),
        Geneset.date.like(f'%{s}%'),
        sa.and_(
            Geneset.showContacts == 1,
            sa.or_(
                Geneset.authorName.like(f'%{s}%'),
                Geneset.authorAffiliation.like(f'%{s}%'),
                Geneset.authorEmail.like(f'%{s}%'),
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
            'genes': [gene.symbol for gene in record.genes],
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

serve_collection_geneset_filtered_datatable = lambda collection_id: serve_datatable(
    lambda sess, collection_id=collection_id: sess.query(Geneset).filter(SetsCollections.type == 1).filter(SetsCollections.collection_id == collection_id).join(SetsCollections, Geneset.id == SetsCollections.set_id),
    [
        (Geneset.id, 'id'),
        (Geneset.enrichrShortId, 'enrichrShortId'),
        (Geneset.enrichrUserListId, 'enrichrUserListId'),
        (Geneset.descrShort, 'descrShort'),
        (Geneset.descrFull, 'descrFull'),
        (Geneset.genes, 'genes'),
        (Geneset.authorName, 'authorName'),
        (Geneset.authorAffiliation, 'authorAffiliation'),
        (Geneset.authorEmail, 'authorEmail'),
        (Geneset.source, 'source'),
        (Geneset.date, 'date'),
        (Geneset.showContacts, 'showContacts'),
        (Geneset.meta, 'meta'),
        (Geneset.category, 'category'),
    ],
    lambda sess, s: sa.or_(
        Geneset.id.in_(
            sess.query(GenesetGene.geneset) \
                .join(Gene, Gene.id == GenesetGene.gene) \
                .filter(Gene.symbol.like(f'{s}%'))
        ),
        Geneset.descrShort.like(f'%{s}%'),
        Geneset.descrFull.like(f'%{s}%'),
        Geneset.source.like(f'%{s}%'),
        Geneset.meta.like(f'%{s}%'),
        Geneset.date.like(f'%{s}%'),
        sa.and_(
            Geneset.showContacts == 1,
            sa.or_(
                Geneset.authorName.like(f'%{s}%'),
                Geneset.authorAffiliation.like(f'%{s}%'),
                Geneset.authorEmail.like(f'%{s}%'),
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
            'genes': [gene.symbol for gene in record.genes],
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