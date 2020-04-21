import requests
import os
from datetime import datetime
from pytz import timezone
from app import geneset

ROOT_PATH = os.environ.get('ROOT_PATH', '/covid19/')


class TestGenesets:
    form = {'source': 'https://amp.pharm.mssm.edu/Enrichr',
            'geneSet': open('gene_list.txt').read(),
            'descrShort': 'Test: Standard submission {}'.format(
                datetime.now(timezone('US/Eastern')).strftime('%Y-%m-%d %H:%M:%S')),
            'descrFull': '',
            'authorName': 'PyTest',
            'authorEmail': 'test@mail.com',
            'authorAff': 'PyTest'}

    def test_add_geneset(self):
        response = geneset.add_geneset(self.form)
        assert response == ('{"success": true}', 200, {'ContentType': 'application/json'})
