import requests
import os
from datetime import datetime
from pytz import timezone
from app import geneset

ROOT_PATH = os.environ.get('ROOT_PATH', '/covid19/')


class TestAddGenesets:
    form = {'source': 'https://amp.pharm.mssm.edu/Enrichr',
            'geneSet': open(os.path.join(os.path.dirname(__file__), 'gene_list.txt')).read(),
            'descrShort': 'Test: Standard submission {}'.format(
                datetime.now(timezone('US/Eastern')).strftime('%Y-%m-%d %H:%M:%S')),
            'descrFull': '',
            'authorName': 'PyTest',
            'authorEmail': 'test@mail.com',
            'authorAff': 'PyTest'}

    def test_add_geneset(self):
        response = geneset.add_geneset(self.form)
        assert response == ('{"success": true}', 200, {'ContentType': 'application/json'})


class TestGetGeneset:
    def test_get_geneset(self):
        assert False


class TestGetGenesets:
    def test_get_genesets(self):
        assert False


class TestApproveGeneset:
    def test_approve_geneset(self):
        assert False