from commands.platform_base import PlatformBase
from domain.domain_schema import DomainSchema


class RegisterApp(PlatformBase):

    def __init__(self, args):
        super().__init__(args)
        self.schema = DomainSchema(args.environment)

    def register(self):
        self.register_domain_schema()
        self.register_core_api()

    def register_domain_schema(self):
        app = self.platform_json['app']
        solution = self.platform_json['solution']
        self.schema.create_solution(solution)
        app_id = self.schema.get_app_id(solution['id_domain'], app['name'])

        if app_id:
            self.schema.update_app(app_id, app, solution, self.get_app_tag())
        else:
            self.schema.create_app(app, solution, self.get_app_tag())

    def register_core_api(self):
        pass