import requests
import os
from datetime import datetime
from pytz import timezone
from app import drugset

ROOT_PATH = os.environ.get('ROOT_PATH', '/covid19/')


class TestDrugsets:
    form = {'source': 'https://github.com/MaayanLab/COVID19DrugsTrendTracker/blob/master/daily_reports',
            'drugSet': open('drug_list.txt').read(),
            'descrShort': 'Test: Standard submission {0}'.format(
                datetime.now(timezone('US/Eastern')).strftime('%Y-%m-%d %H:%M:%S')),
            'descrFull': '',
            'authorName': 'PyTest',
            'authorEmail': 'test@mail.com',
            'authorAff': 'PyTest'}

    def test_add_drugset(self):
        response = drugset.add_drugset(self.form)
        assert response == ('{"success": true}', 200, {'ContentType': 'application/json'})
