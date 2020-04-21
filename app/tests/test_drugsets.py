import requests
import os
from datetime import datetime
from pytz import timezone

ROOT_PATH = os.environ.get('ROOT_PATH', '/covid19/')


class TestDrugsets:
    def test_submit(self):
        url = 'http://0.0.0.0:8080/covid19/drugsets'
        payload = {'source': 'https://github.com/MaayanLab/COVID19DrugsTrendTracker/blob/master/daily_reports',
                   'drugSet': open('drug_list.txt').read(),
                   'descrShort': 'Test: Standard submission {0}'.format(datetime.now(timezone('US/Eastern')).strftime('%Y-%m-%d %H:%M:%S')),
                   'descrFull': '',
                   'authorName': 'PyTest',
                   'authorEmail': 'test@mail.com',
                   'authorAff': 'PyTest'}

        response = requests.request("POST", url, data=payload)
        assert response.status_code == 200
