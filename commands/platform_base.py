import json
import settings

from env_docker import DockerAppDeploy
from env_openshift import OpenShiftAppDeploy


class PlatformBase:

    def __init__(self, args):
        self.environment = self.get_platform(args)
        self.load_platform_json(args)

    def load_platform_json(self, args):
        with open(args.config_json) as json_file:
            self.platform_json = json.load(json_file)

    def is_presentation(self):
        return self.platform_json['app']['type'] == 'presentation'

    def get_tag_name(self):
        return self.platform_json['app']['version']

    def get_app_tag(self):
        return '{app}:{tag}'.format(app=self.get_app(), tag=self.get_tag_name())

    def get_app(self):
        return self.platform_json['app']['container']

    def get_app_process_id(self):
        return self.platform_json['app']['id']

    def get_system_id(self):
        return self.platform_json['solution']['id']

    def get_platform(self, args):
        return {
            'docker': DockerAppDeploy,
            'openshift': OpenShiftAppDeploy
        }[args.platform](settings)

    def _get_labels(self):
        return {
            'app_name': self.get_app(),
            'system_id': self.get_system_id(),
            'process_id': self.get_app_process_id()
        }