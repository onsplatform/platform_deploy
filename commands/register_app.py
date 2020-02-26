from commands.platform_base import PlatformBase
from domain.domain_schema import DomainSchema
from core_api.core_api import CoreApi


class RegisterApp(PlatformBase):

    def __init__(self, args):
        super().__init__(args)
        self.solution = self.platform_json['solution']
        self.app = self.platform_json['app']

        self.schema = DomainSchema(args.environment)
        self.core_api = CoreApi(args.environment)

    def register(self):
        self.__register_domain_schema(self.solution.copy(), self.app.copy())
        self.__register_core_api(self.solution.copy(), self.app.copy())

    def __register_domain_schema(self, solution, app):
        solution_return = self.schema.create_solution(solution)
        if solution_return and solution_return.status_code == 200 and len(solution_return) > 0:
            print('Solution Created')
        else:
            print('Solution not Created')

        app_id = self.schema.get_app_id(solution['id_domain'], app['name'])
        if app_id:
            self.schema.update_app(app_id, app, solution,
                                   self.get_app_and_tag())
            print('App Updated')
        else:
            self.schema.create_app(app, solution, self.get_app_and_tag())
            print('App Created')

    def __register_core_api(self, solution, app):
        self.core_api.register_solution(solution)
        print('Registered Solution in Core Api')

        self.core_api.register_app(app, solution)
        print('Registered Application in Core Api')

        self.core_api.upload_maps(solution, app)
        print('Maps Uploaded in Core Api')

        self.core_api.upload_operations(solution, app)
        print('Metadata Uploaded in Core Api')
