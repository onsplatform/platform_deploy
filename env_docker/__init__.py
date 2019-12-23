import docker

from docker.errors import APIError
from random import randint


class DockerAppDeploy():

    def __init__(self, settings):
        self.client = docker.from_env()
        self.registry = settings.REGISTRY['uri']

    def build_image(self, app_tag, labels):
        build = self.client.images.build(path='.', tag=app_tag, labels=labels, nocache=True)
        if build:
            return build[0]

    def tag(self, image, tag_name, app):
        return image.tag(repository=self._get_repository(app), tag=tag_name)

    def push_image(self, app):
        self.client.images.push(repository=self._get_repository(app))

    def rm(self, app):
        try:
            container = self.client.containers.get(app)
            container.remove()
        except APIError:
            print('docker.errors.APIError at remove()')

    def run(self, image, app_name, variables, labels):
        self.client.containers.run(
            image=image,
            labels=labels,
            environment=variables,
            network='plataforma_network',
            ports={"7" + str(randint(100, 999)): 9229},
            name=app_name
        )

    def _get_repository(self, app):
        return '{registry}/{app}'.format(registry=self.registry, app=app)
