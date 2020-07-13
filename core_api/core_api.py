import yaml
from os import listdir, getcwd
from os.path import isfile, join, exists

import settings
from platform_sdk.core_api import core_system_solution, core_app, core_map, core_metadata


class CoreApi:

    def __init__(self, environment):
        self.environment = environment
        self.url = settings.CORE_API[environment]['uri']

    def register_solution(self, solution):
        core_api_solution = core_system_solution.SystemSolution(self.url)
        solution_result = core_api_solution.find_by_id(solution['id'])
        if len(solution_result.content) == 0:
            solution_result = core_api_solution.create(solution)
        return solution_result.content

    def register_app(self, app, solution):
        core_api_app = core_app.App(self.url)
        app_result = core_api_app.find_by_id(app['id'])
        app['systemId'] = solution['id']
        if len(app_result.content) == 0:
            app_result = core_api_app.create(app)
        return app_result.content

    def upload_maps(self, solution, app):
        path = getcwd() + '/Mapa/'
        if exists(path):
            map_names = self.__list_yaml_files(path)
            map_yml = self._get_yaml(map_names, path)
            map_result = core_map.Map(self.url).create({
                'content': map_yml,
                'name': app['name'],
                'systemId': solution['id'],
                'processId': app['id'],
                'version': app['version']
            })
            return map_result.content

    def upload_operations(self, solution, app):
        path = getcwd() + '/Metadados/'
        if exists(path):
            metadata_names = self.__list_yaml_files(path)
            metadata_yml = self._get_yaml_to_dict(metadata_names, path)[0]
            operations = []
            for operation in metadata_yml['operations']:
                # TODO: Create class/interface to load platform.json
                operation['systemId'] = solution['id']
                operation['processId'] = app['id']
                operation['event_in'] = operation['event']
                operation['event_out'] = operation['name'] + '.done'
                operation['version'] = app['version']
                operation['reprocessable'] = operation.get('reprocessOnDeploy', False)
                operation['image'] = '{0}:{1}'.format(app['container'], app['version'])
                operations.append(operation)
            core_operations = core_metadata.Metadata(self.url)
            operations_result = core_operations.create(operations)

            return operations_result.content

    def __list_yaml_files(self, path):
        return [f for f in listdir(path) if isfile(join(path, f)) and (f.endswith('.yaml') or f.endswith('.yml'))]

    def _get_yaml_to_dict(self, file_names, folder):
        file_list = []
        for file in file_names:
            with open(folder + file, 'r') as stream:
                try:
                    yaml_file = yaml.safe_load(stream)
                    file_list.append(yaml_file)
                except yaml.YAMLError as exc:
                    print(exc)
        return file_list

    def _get_yaml(self, file_names, folder):
        yaml = ''
        for file in file_names:
            yaml += open(folder + file, 'r').read()
        return yaml

