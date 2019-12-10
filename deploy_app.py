import json

from docker_env import DockerAppDeploy
from openshift_env import OpenShiftAppDeploy


class DeployApp:

    def __init__(self):
        self.platform_json = ''

    def register_app(self, args):
        self.load_platform_json(args)
        self.deploy_app(args)

    def deploy_app(self, args):
        environment = self.get_platform(args.environment)
        image = environment.build_image()
        environment.deploy(image.id)

    def load_platform_json(self, args):
        with open(args.config_json) as json_file:
            self.platform_json = json.load(json_file)

    def get_platform(self, platform):
        return {
            'docker': DockerAppDeploy,
            'openshift': OpenShiftAppDeploy
        }[platform](self.platform_json)
