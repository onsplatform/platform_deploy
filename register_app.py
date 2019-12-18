from platform_base import PlatformBase
from domain.domain_schema import DomainSchema


class RegisterApp(PlatformBase):

    def __init__(self, args):
        super().__init__(args)
        self.schema = DomainSchema(args.environment)

    def register(self):
        app = self.platform_json['app']
        solution = self.platform_json['solution']
        self.schema.update_solution(solution)
        app_id = self.schema.get_app_id(solution['id'], app['name'])

        if app_id:
            app['id'] = app_id
            self.schema.update_app(app, solution, self.get_app_tag())
        else:
            self.schema.create_app(app, solution, self.get_app_tag())
