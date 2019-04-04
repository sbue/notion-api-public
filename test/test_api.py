import unittest
from urllib.parse import urlencode
from flask import url_for

import api


class TestAPI(unittest.TestCase):

    def setUp(self):
        api.app.config['TESTING'] = True
        self.client = api.app.test_client()

    def run_command(self, command_name, qs):
        with api.app.test_request_context():
            self.client.get(f'{url_for("api_for_command", command_name=command_name)}?{urlencode(qs)}')

    def test_new_day(self):
        self.run_command('new-metrics', {'days_from_today': '0'})
