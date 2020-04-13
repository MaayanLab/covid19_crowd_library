import json
import requests

import sqlalchemy as sa
from app.database import Session
from app.models import Geneset, GenesetGene, Gene, gene_splitter
from app.datatables import serve_datatable
from app.utils import match_meta


def enrichr_submit(geneset, short_description):
    payload = {
        'list': (None, '\n'.join(geneset)),
        'description': (None, short_description)
    }
    response = requests.post('http://amp.pharm.mssm.edu/Enrichr/addList', files=payload)
    if not response.ok:
        raise Exception('Error analyzing gene list')
    return json.loads(response.text)


def add_geneset(form):
    source = form['source']
    gene_set = gene_splitter.split(form['geneSet'])
    descr_full = form['descrFull']
    desc_short = form['descrShort']
    author_name = form['authorName']
    author_email = form['authorEmail']
    author_aff = form['authorAff']
    show_contacts = 1 if 'showContacts' in form else 0
    enrichr_ids = enrichr_submit(gene_set, desc_short)
    enrichr_shortid = enrichr_ids['shortId']
    enrichr_userlistid = enrichr_ids['userListId']
    meta = {}

    # '-show_contacts' is correction for, well, show_contacts presence
    if len(form) - show_contacts > 9:
        meta = match_meta(form, 9)

    try:
        sess = Session()
        sess.add(
            Geneset.create(
                sess,
                enrichrShortId=enrichr_shortid,
                enrichrUserListId=enrichr_userlistid,
                descrShort=desc_short,
                descrFull=descr_full,
                authorName=author_name,
                authorAffiliation=author_aff,
                authorEmail=author_email,
                showContacts=show_contacts,
                genes=gene_set,
                source=source,
                meta=meta,
            )
        )
        sess.commit()
        sess.close()
        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
    except Exception as e:
        return json.dumps({'success': False, 'error': str(e)}), 500, {'ContentType': 'application/json'}


def get_geneset(id):
    try:
        sess = Session()
        r = sess.query(Geneset).filter(Geneset.id == id).first().jsonify()
        sess.close()
        return json.dumps(r, default=str), 200, {'ContentType': 'application/json'}
    except Exception as e:
        return json.dumps({'error': str(e)}), 404, {'ContentType': 'application/json'}


def get_genesets(reviewed=1):
    try:
        sess = Session()
        r = [g.jsonify() for g in sess.query(Geneset).filter(Geneset.reviewed == reviewed)]
        sess.close()
        return json.dumps(r, default=str), 200, {'ContentType': 'application/json'}
    except Exception as e:
        return json.dumps({'error': str(e)}), 404, {'ContentType': 'application/json'}


def approve_geneset(form):
    geneset_id = form['id']
    reviewed = form['reviewed']
    try:
        sess = Session()
        geneset = sess.query(Geneset).get(geneset_id)
        geneset.reviewed = reviewed
        sess.commit()
        sess.close()
        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
    except Exception as e:
        return json.dumps({'success': False, 'error': str(e)}), 200, {'ContentType': 'application/json'}

serve_geneset_datatable = lambda reviewed: serve_datatable(
    lambda sess, reviewed=reviewed: sess.query(Geneset).filter(Geneset.reviewed == reviewed),
    [
        (Geneset.id, 'id'),
        (Geneset.descrShort, 'descrShort'),
        (Geneset.descrFull, 'descrFull'),
        (Geneset.genes, 'genes'),
        (Geneset.enrichrShortId, 'enrichrShortId'),
        (Geneset.authorName, 'authorName'),
        (Geneset.authorAffiliation, 'authorAffiliation'),
        (Geneset.authorEmail, 'authorEmail'),
        (Geneset.source, 'source'),
        (Geneset.date, 'date'),
        (Geneset.showContacts, 'showContacts'),
        (Geneset.meta, 'meta'),
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
        sa.and_(
            Geneset.showContacts == 1,
            Geneset.authorName.like(f'%{s}%'),
            Geneset.authorAffiliation.like(f'%{s}%'),
            Geneset.authorEmail.like(f'%{s}%'),
        ),
    ),
    lambda qs, reviewed=reviewed: [
        {
            'id': record.id,
            'descrShort': record.descrShort,
            'descrFull': record.descrFull,
            'genes': [gene.symbol for gene in record.genes],
            'enrichrShortId': record.enrichrShortId,
            'authorName': record.authorName if record.showContacts or reviewed == 0 else '',
            'authorAffiliation': record.authorAffiliation if record.showContacts or reviewed == 0 else '',
            'authorEmail': record.authorEmail if record.showContacts or reviewed == 0 else '',
            'source': record.source,
            'date': record.date,
            'showContacts': record.showContacts,
            'meta': record.meta,
        }
        for record in qs
    ]
)
