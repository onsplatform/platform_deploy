import settings

from env_docker import DockerAppDeploy
from env_openshift import OpenShiftAppDeploy
from platform_base import PlatformBase


class BuildApp(PlatformBase):

    def __init__(self, args):
        super().__init__(args)
        self.environment = self.get_platform(args)

    def build(self):
        image = self.environment.build_image()
        if image and self.environment.tag(image):
            self.environment.push_image()

    def get_platform(self, args):
        return {
            'docker': DockerAppDeploy,
            'openshift': OpenShiftAppDeploy
        }[args.platform](settings, args)
