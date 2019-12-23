import requests
import json

import settings


class DomainSchema:
    headers = {'content-type': 'application/json'}

    def __init__(self, environment):
        self.url = settings.SCHEMA[environment]['uri']

    def create_solution(self, solution):
        response = requests.post(url=self.url + 'solution/', data=json.dumps(solution), headers=self.headers)
        return response.json()

    def get_app_id(self, solution_id, name):
        response = requests.get(url=self.url + 'app/{solution_id}/{name}'.format(solution_id=solution_id, name=name))
        response_json = response.json()
        if response.status_code == 200 and len(response_json) > 0:
            return response_json[0]['id']

    def create_app(self, app, solution, tag):
        new_app = self._get_app_from_config(app, solution)
        response = requests.post(url=self.url + 'app/', data=json.dumps(new_app), headers=self.headers)
        response_json = response.json()
        app['process_id'] = app['id']
        app['id'] = response_json['id']
        self.create_app_version(app, tag)
        return response_json

    def update_app(self, app_id, app, solution, tag):
        new_app = self._get_app_from_config(app, solution)
        new_app['id'] = app_id
        response = requests.put(url=self.url + 'app/{id}/'.format(id=new_app['id']), data=json.dumps(new_app),
                                headers=self.headers)
        app['process_id'] = app['id']
        app['id'] = app_id
        self.create_app_version(app, tag)
        return response.json()

    def create_app_version(self, app, tag):
        new_app_version = self._get_app_version_from_config(app, tag)
        new_app_version['app_id'] = app['id']
        response = requests.post(url=self.url + 'appversion/', data=json.dumps(new_app_version), headers=self.headers)
        return response.json()

    def _get_app_version_from_config(self, app, tag):
        return {
            'version': app['version'],
            'tag': tag,
            'date_begin_validity': app['date_begin_validity'],
            'date_end_validity': app['date_end_validity'],
            'process_id': app['process_id'],
        }

    def _get_app_from_config(self, app, solution):
        return {
            'name': app['name'],
            'solution_id': solution['id_domain'],
            'container': app['container'],
            'type': app['type'],
            'technology': app['tecnology']
        }
