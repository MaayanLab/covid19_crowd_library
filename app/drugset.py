import json

from app.database import Session
from app.models import Drugset, drug_splitter


def add_drugset(form):
    source = form['source']
    drug_set = drug_splitter.split(form['drugSet'])
    descr_full = form['descrFull']
    desc_short = form['descrShort']
    author_name = form['authorName']
    author_email = form['authorEmail']
    author_aff = form['authorAff']
    show_contacts = 1 if 'showContacts' in form else 0

    try:
        sess = Session()
        sess.add(
            Drugset(
                descrShort=desc_short,
                descrFull=descr_full,
                authorName=author_name,
                authorAffiliation=author_aff,
                authorEmail=author_email,
                showContacts=show_contacts,
                drugs=drug_set,
                source=source
            )
        )
        sess.commit()
        sess.close()
        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
    except Exception as e:
        return json.dumps({'success': False, 'error': str(e)}), 500, {'ContentType': 'application/json'}


def get_drugset(id):
    try:
        sess = Session()
        r = sess.query(Drugset).filter(Drugset.id == id).first().jsonify()
        sess.close()
        return json.dumps(r, default=str), 200, {'ContentType': 'application/json'}
    except Exception as e:
        return json.dumps({'error': str(e)}), 404, {'ContentType': 'application/json'}


def get_drugsets(reviewed=1):
    try:
        sess = Session()
        r = [g.jsonify() for g in sess.query(Drugset).filter(Drugset.reviewed == reviewed)]
        sess.close()
        return json.dumps(r, default=str), 200, {'ContentType': 'application/json'}
    except Exception as e:
        return json.dumps({'error': str(e)}), 404, {'ContentType': 'application/json'}


def approve_drugset(form):
    drugset_id = form['id']
    reviewed = form['reviewed']
    try:
        sess = Session()
        drugset = sess.query(Drugset).get(drugset_id)
        drugset.reviewed = reviewed
        sess.commit()
        sess.close()
        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
    except Exception as e:
        return json.dumps({'success': False, 'error': str(e)}), 200, {'ContentType': 'application/json'}
