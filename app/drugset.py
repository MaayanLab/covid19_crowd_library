import json
import traceback
from itertools import combinations
import sqlalchemy as sa
from app.database import Session
from app.models import Drugset, DrugsetDrug, Drug, drug_splitter
from app.datatables import serve_datatable
from app.utils import match_meta, enrichr_submit


def add_drugset(form):
    source = form['source']
    drug_set = list(filter(None, (drug.strip() for drug in drug_splitter.split(form['drugSet']))))
    descr_full = form['descrFull']
    desc_short = form['descrShort']
    author_name = form['authorName']
    author_email = form['authorEmail']
    author_aff = form['authorAff']
    show_contacts = 1 if 'showContacts' in form else 0
    enrichr_ids = enrichr_submit(drug_set, desc_short, 'DrugEnrichr')
    enrichr_shortid = enrichr_ids['shortId']
    enrichr_userlistid = enrichr_ids['userListId']
    meta = {}

    if 'experimental' in form and form['experimental'] == 'on':
        category = 2
    elif 'computational' in form and form['computational'] == 'on':
        category = 3
    elif 'twitter' in form and form['twitter'] == 'on':
        category = 4
    else:
        category = 1

    # '-show_contacts' is correction for, well, show_contacts presence
    if len(form) - show_contacts > 7:
        meta = match_meta(form, 7)

    try:
        sess = Session()
        sess.add(
            Drugset.create(
                sess,
                enrichrShortId=enrichr_shortid,
                enrichrUserListId=enrichr_userlistid,
                descrShort=desc_short,
                descrFull=descr_full,
                authorName=author_name,
                authorAffiliation=author_aff,
                authorEmail=author_email,
                showContacts=show_contacts,
                drugs=drug_set,
                source=source,
                meta=meta,
                category=category,
            )
        )
        sess.commit()
        sess.close()
        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
    except Exception as e:
        traceback.print_exc()
        return json.dumps({'success': False, 'error': str(e)}), 500, {'ContentType': 'application/json'}


def get_drugset(id):
    try:
        sess = Session()
        r = sess.query(Drugset).filter(Drugset.id == id).first().jsonify()
        sess.close()
        return json.dumps(r, default=str), 200, {'ContentType': 'application/json'}
    except Exception as e:
        traceback.print_exc()
        return json.dumps({'error': str(e)}), 404, {'ContentType': 'application/json'}


def get_drug(name):
    try:
        sess = Session()
        r = {'name': name, 'sets': [{'id': drugset.id, 'name': drugset.descrShort}
                                    for drugset in sess.query(Drugset) \
                                        .join(DrugsetDrug, Drugset.id == DrugsetDrug.drugset) \
                                        .join(Drug, DrugsetDrug.drug == Drug.id) \
                                        .filter(Drug.symbol == name,
                                                Drugset.reviewed == 1,
                                                sa.or_(Drugset.category == 2, Drugset.category == 3))]}
        #
        # drug = sess.query(Drug).filter(Drug.symbol == name).first()
        # drugset_ids = sess.query(DrugsetDrug).filter(DrugsetDrug.drug == drug.id)
        # r = {'name': name, 'sets': []}
        # for drugset_id in drugset_ids:
        #     drugset = sess.query(Drugset)\
        #         .filter(Drugset.id == drugset_id.drugset)\
        #         .filter(sa.or_(Drugset.category == 2, Drugset.category == 3))\
        #         .filter(Drugset.reviewed == 1)\
        #         .first()
        #     if drugset:
        #         r['sets'].append({'id': drugset.id, 'name': drugset.descrShort})
        sess.close()
        return json.dumps(r, default=str), 200, {'ContentType': 'application/json'}
    except Exception as e:
        traceback.print_exc()
        return json.dumps({'error': str(e)}), 404, {'ContentType': 'application/json'}


def twitter_drug_submission(name):
    try:
        sess = Session()
        drug = sess.query(Drug).filter(Drug.symbol == name).first()
        drugset_ids = sess.query(DrugsetDrug).filter(DrugsetDrug.drug == drug.id)
        r = []
        for drugset_id in drugset_ids:
            date = sess.query(sa.cast(Drugset.date, sa.Date)) \
                .filter(Drugset.id == drugset_id.drugset) \
                .filter(Drugset.category == 4) \
                .filter(Drugset.reviewed == 1).first()
            if date:
                r.append({'count': 1, 'date': date[0]})
        sess.close()
        return json.dumps(r, default=str), 200, {'ContentType': 'application/json'}
    except Exception as e:
        traceback.print_exc()
        return json.dumps({'error': str(e)}), 404, {'ContentType': 'application/json'}


def get_drugsets(reviewed=1):
    try:
        sess = Session()
        r = [g.jsonify() for g in sess.query(Drugset).filter(Drugset.reviewed == reviewed)]
        sess.close()
        return json.dumps(r, default=str), 200, {'ContentType': 'application/json'}
    except Exception as e:
        traceback.print_exc()
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
        traceback.print_exc()
        return json.dumps({'success': False, 'error': str(e)}), 500, {'ContentType': 'application/json'}


def change_category(form):
    drugset_id = form['id']
    category = form['category']
    try:
        sess = Session()
        drugset = sess.query(Drugset).get(drugset_id)
        drugset.category = category
        sess.commit()
        sess.close()
        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
    except Exception as e:
        traceback.print_exc()
        return json.dumps({'success': False, 'error': str(e)}), 500, {'ContentType': 'application/json'}


serve_drugset_datatable = lambda reviewed: serve_datatable(
    lambda sess, reviewed=reviewed: sess.query(Drugset).filter(Drugset.reviewed == reviewed).order_by(
        sa.desc(Drugset.date)),
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
    lambda qs, reviewed=reviewed: [
        {
            'id': record.id,
            'enrichrShortId': record.enrichrShortId,
            'enrichrUserListId': record.enrichrUserListId,
            'descrShort': record.descrShort,
            'descrFull': record.descrFull,
            'drugs': [gene.symbol for gene in record.drugs],
            'authorName': record.authorName if record.showContacts or reviewed == 0 else '',
            'authorAffiliation': record.authorAffiliation if record.showContacts or reviewed == 0 else '',
            'authorEmail': record.authorEmail if record.showContacts or reviewed == 0 else '',
            'source': record.source,
            'date': record.date,
            'showContacts': record.showContacts,
            'meta': record.meta,
            'category': record.category,
        }
        for record in qs
    ]
)

serve_drugset_filtered_datatable = lambda reviewed, category: serve_datatable(
    lambda sess, reviewed=reviewed: sess.query(Drugset).filter(Drugset.reviewed == reviewed).filter(
        Drugset.category == category).order_by(sa.desc(Drugset.date)),
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
    lambda qs, reviewed=reviewed: [
        {
            'id': record.id,
            'enrichrShortId': record.enrichrShortId,
            'enrichrUserListId': record.enrichrUserListId,
            'descrShort': record.descrShort,
            'descrFull': record.descrFull,
            'drugs': [gene.symbol for gene in record.drugs],
            'authorName': record.authorName if record.showContacts or reviewed == 0 else '',
            'authorAffiliation': record.authorAffiliation if record.showContacts or reviewed == 0 else '',
            'authorEmail': record.authorEmail if record.showContacts or reviewed == 0 else '',
            'source': record.source,
            'date': record.date,
            'showContacts': record.showContacts,
            'meta': record.meta,
            'category': record.category,
        }
        for record in qs
    ]
)


def get_intersection(ids=[]):
    drugsets = []
    labels = []
    for drugset_id in ids:
        drugset = json.loads(get_drugset(drugset_id)[0])
        labels.append(drugset["descrShort"])
        drugsets.append(drugset)
    overlaps = []
    for i in range(len(drugsets)):
        combo = combinations(drugsets, r=i + 1)
        for c in combo:
            data = {
                "sets": []
            }
            for d in c:
                data["sets"].append(d["descrShort"])
                if not "intersection" in data:
                    data["intersection"] = set(d["drugs"])
                else:
                    data["intersection"] = data["intersection"].intersection(d["drugs"])
            data["intersection"] = list(data["intersection"])
            data["size"] = len(data["intersection"])
            overlaps.append(data)
    return {"overlaps": overlaps, "labels": labels}
