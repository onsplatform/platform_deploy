from platform_sdk.core_api import SystemCore
import settings

from os import listdir,getcwd
from os.path import isfile, join
import yaml

from pprint import pprint
class CoreApi:

    def __init__(self, environment):
        self.environment = environment
        self.url = settings.CORE_API[environment]['uri']

    def register_solution(self,solution):
        system_core = SystemCore(self.url,'system')
        solution_result = system_core.find_by_id(solution['id'])    
        if len(solution_result.content) == 0:
            solution_result = system_core.create(solution)
        return solution_result.content

    def register_app(self, app):
        system_core = SystemCore(self.url,'installedApp')
        app_result = system_core.find_by_id(app['id'])      
        if len(app_result.content) == 0:
            app_result = system_core.create(app)
        return app_result.content

    def upload_maps(self, solution,app):
        path = getcwd() + '/Mapa/'
        map_names = self.__list_yaml_files(path)
        map_yml = self.__get_files(map_names,path)[0]
        map_yml['systemId'] = solution['id']
        map_yml['processId'] = app['id']
        # map_yml['reprocess'] = True
        breakpoint()

        system_core = SystemCore(self.url,'map')
        map_result = system_core.create(map_yml)
        pprint(map_result.content)

        return map_result.content

    def upload_operations(self,solution,app):
        
        path = getcwd() + '/Metadados/'
        metadata_names = self.__list_yaml_files(path)
        metadata_yml = self.__get_files(metadata_names,path)[0]
        operations = []
        for operation in metadata_yml['operations']:
            
            operation['systemId'] = solution['id']
            operation['processId'] = app['id']
            operation['event_in'] = operation['event']
            operation['event_out'] = operation['name'] + '.done'
            operations.append(operation)
        system_core = SystemCore(self.url,'operation')
        breakpoint()
        operations_result = system_core.create(operations)
        # pprint(operations_result.content)
        return operations_result.content
        
    def __list_yaml_files(self,path):
        return [f for f in listdir(path) if isfile(join(path, f)) and (f.endswith('.yaml') or f.endswith('.yml'))]

    def __get_files(self,file_names,folder):
        file_list = []
        for file in file_names:
            with open(folder+file, 'r') as stream:
                try:
                    yaml_file = yaml.safe_load(stream)
                    file_list.append(yaml_file)
                except yaml.YAMLError as exc:
                    print(exc)
        return file_list