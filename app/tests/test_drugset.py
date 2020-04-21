import os
from datetime import datetime
from pytz import timezone
from app import drugset

ROOT_PATH = os.environ.get('ROOT_PATH', '/covid19/')


class TestAddDrugsets:
    form = {'source': 'https://github.com/MaayanLab/COVID19DrugsTrendTracker/blob/master/daily_reports',
            'drugSet': open(os.path.join(os.path.dirname(__file__), 'drug_list.txt')).read(),
            'descrShort': 'Test: Standard submission {0}'.format(
                datetime.now(timezone('US/Eastern')).strftime('%Y-%m-%d %H:%M:%S')),
            'descrFull': '',
            'authorName': 'PyTest',
            'authorEmail': 'test@mail.com',
            'authorAff': 'PyTest'}

    def test_add_drugset(self):
        response = drugset.add_drugset(self.form)
        assert response == ('{"success": true}', 200, {'ContentType': 'application/json'})


class TestGetDrugset:
    def test_get_drugset(self):
        assert False


class TestApproveDrugset:
    def test_approve_drugset(self):
        assert False