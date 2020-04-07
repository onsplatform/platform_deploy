import requests
import json

import settings


class DiscoveryReprocess:
    headers = {'content-type': 'application/json'}

    def __init__(self, environment):
        self.url = settings.DISCOVERY[environment]['uri']

    def force_reprocess(self, app, solution):
        discovery = {
            "date_begin_validity": app['date_begin_validity'],
            "date_end_validity": app['date_end_validity'],
            "process_id": app['id'],
            "solution": solution['name']
        }

        response = requests.post(url=self.url + 'force_reprocess/', data=json.dumps(discovery), headers=self.headers)
        return response.status_code == 200
