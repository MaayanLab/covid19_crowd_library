from sqlalchemy import *
import os
import json
import requests

user = os.environ.get('DB_USER', 'enrichr')
password = os.environ.get('DB_PASSWORD')
host = os.environ.get('HOST')
db = os.environ.get('DB')
engine = create_engine('mysql+pymysql://{0}:{1}@{2}/{3}'.format(user, password, host, db), pool_recycle=300)
metadata = MetaData()
enrichr_covid = Table('genesets', metadata,
                      Column('id', Integer, primary_key=True),
                      Column('enrichrShortId', String(255), nullable=False),
                      Column('enrichrUserListId', Integer, nullable=False),
                      Column('genes', Text, nullable=False),
                      Column('descrShort', String(255), nullable=False),
                      Column('descrFull', String(255), nullable=False),
                      Column('authorName', String(255), nullable=False),
                      Column('authorAffiliation', String(255)),
                      Column('authorEmail', String(255)),
                      Column('showContacts', Integer, nullable=False),
                      )


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
    gene_list = form['geneList']
    descr_full = form['descrFull']
    desc_short = form['descrShort']
    author_name = form['aurthorName']
    author_email = form['authorEmail']
    author_aff = form['authorAff']
    show_contacts = form['showContacts']
    enrichr_ids = enrichr_submit(gene_list, desc_short)
    enrichr_shortid = enrichr_ids['shortId']
    enrichr_userlistid = enrichr_ids['userListId']

    engine.execute(
        enrichr_covid.insert(),
        {'enrichrShortId': enrichr_shortid,
         'enrichrUserListId': enrichr_userlistid,
         'descrShort': desc_short,
         'descrFull': descr_full,
         'authorName': author_name,
         'authorAffiliation': author_aff,
         'authorEmail': author_email,
         'showContacts': show_contacts,
         'genes': gene_list
         }
    )
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


def get_geneset(user_list_id):
    response = requests.get('http://amp.pharm.mssm.edu/Enrichr/view?userListId={}'.format(user_list_id))
    if not response.ok:
        raise Exception('Error getting gene list')

    data = json.loads(response.text)
    print(data)
    return None


def get_genesets():
    return None
