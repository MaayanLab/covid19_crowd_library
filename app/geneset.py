import json

import requests

from app.database import Session
from app.models import Geneset


def enrichr_submit(genelist, short_description):
    payload = {
        'list': (None, genelist),
        'description': (None, short_description)
    }
    response = requests.post('http://amp.pharm.mssm.edu/Enrichr/addList', files=payload)
    if not response.ok:
        raise Exception('Error analyzing gene list')
    return json.loads(response.text)


def add_geneset(form):
    source = form['source']
    gene_list = form['geneList']
    descr_full = form['descrFull']
    desc_short = form['descrShort']
    author_name = form['authorName']
    author_email = form['authorEmail']
    author_aff = form['authorAff']
    show_contacts = 1 if 'showContacts' in form else 0
    enrichr_ids = enrichr_submit(gene_list, desc_short)
    enrichr_shortid = enrichr_ids['shortId']
    enrichr_userlistid = enrichr_ids['userListId']

    try:
        sess = Session()
        sess.add(
            Geneset(
                enrichrShortId=enrichr_shortid,
                enrichrUserListId=enrichr_userlistid,
                descrShort=desc_short,
                descrFull=descr_full,
                authorName=author_name,
                authorAffiliation=author_aff,
                authorEmail=author_email,
                showContacts=show_contacts,
                genes=gene_list,
                source=source
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
        return json.dumps(r), 200, {'ContentType': 'application/json'}
    except Exception as e:
        return json.dumps({'error': str(e)}), 404, {'ContentType': 'application/json'}


def get_genesets(reviewed=1):
    try:
        sess = Session()
        r = [g.jsonify() for g in sess.query(Geneset).filter(Geneset.reviewed == reviewed)]
        sess.close()
        return json.dumps(r), 200, {'ContentType': 'application/json'}
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
