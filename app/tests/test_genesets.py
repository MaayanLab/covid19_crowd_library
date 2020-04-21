import requests
import os
from datetime import datetime
from pytz import timezone

ROOT_PATH = os.environ.get('ROOT_PATH', '/covid19/')


class TestGenesets:
    def test_submit(self):
        url = 'http://0.0.0.0:8080/covid19/genesets'
        payload = {'source': 'https://amp.pharm.mssm.edu/Enrichr',
                   'geneSet': open('gene_list.txt').read(),
                   'descrShort': 'Test: Standard submission {}'.format(datetime.now(timezone('US/Eastern')).strftime('%Y-%m-%d %H:%M:%S')),
                   'descrFull': '',
                   'authorName': 'PyTest',
                   'authorEmail': 'test@mail.com',
                   'authorAff': 'PyTest'}

        response = requests.request("POST", url, data=payload)
        assert response.status_code == 200
