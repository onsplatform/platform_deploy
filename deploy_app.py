import json
import os

from docker_env import DockerAppDeploy
from openshift_env import OpenShiftAppDeploy


class DeployApp:

    platform_json = ''
    REGISTRY = os.environ.setdefault('IMAGE_REGISTRY', 'localhost:5000')

    def register_app(self, args):
        self.load_platform_json(args)
        self.deploy_app(args)

    def deploy_app(self, args):
        environment = self.get_platform(args.environment)
        image = environment.build_image()
        environment.tag(image)
        environment.push_image()
        # call api core
        # call domain schema
        if self.platform_json['app']['type'] == 'presentation':
            environment.rm()
            environment.run(image.id, {
                'API_MODE': True,
                'SYSTEM_ID': self.platform_json['solution']['id']
            })

    def load_platform_json(self, args):
        with open(args.config_json) as json_file:
            self.platform_json = json.load(json_file)

    def get_platform(self, platform):
        return {
            'docker': DockerAppDeploy,
            'openshift': OpenShiftAppDeploy
        }[platform](self.platform_json, self.REGISTRY)