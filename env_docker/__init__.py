import docker

from docker.errors import APIError
from random import randint

from platform_base import PlatformBase


class DockerAppDeploy(PlatformBase):

    def __init__(self, settings, args):
        super().__init__(args)
        self.client = docker.from_env()
        self.registry = settings.REGISTRY['uri']

    def build_image(self):
        build = self.client.images.build(path='.', tag=self.get_app_tag(), labels=self._get_labels(), nocache=True)
        if build:
            return build[0]

    def tag(self, image):
        return image.tag(repository=self._get_repository(), tag=self.get_tag_name())

    def push_image(self):
        self.client.images.push(repository=self._get_repository())

    def rm(self):
        try:
            container = self.client.containers.get(self.get_app())
            container.remove()
        except APIError:
            print('docker.errors.APIError at remove()')

    def run(self, image, variables):
        self.client.containers.run(
            image=image,
            labels=dict(self._get_labels(), **self._get_traefik_labels()),
            environment=variables,
            network='plataforma_network',
            ports={"7" + str(randint(100, 999)): 9229},
            name=self.get_app()
        )

    def _get_labels(self):
        return {
            'app_name': self.get_app(),
            'system_id': self.platform_json['solution']['id'],
            'process_id': self.platform_json['app']['id']
        }

    def _get_traefik_labels(self):
        return {
            'traefik.backend': self.get_app(),
            'traefik.' + self.get_app() + '.frontend.rule': 'PathPrefixStrip: /' + self.get_app(),
            'traefik.docker.network': 'plataforma_network',
            'traefik.port': '8088'
        }

    def _get_repository(self):
        return '{registry}/{app}'.format(registry=self.registry, app=self.get_app())
