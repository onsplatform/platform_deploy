import docker

from docker.errors import APIError
from random import randint


class DockerAppDeploy():

    def __init__(self, settings):
        self.client = docker.from_env()
        self.registry = settings.REGISTRY['uri']
        self.registry_username = settings.REGISTRY['username']
        self.registry_password = settings.REGISTRY['password']

    def build_image(self, app_tag, labels):
        build = self.client.images.build(
            path='.', tag=app_tag, labels=labels, nocache=True)
        if build:
            return build[0]

    def tag(self, image, tag_name, app):
        return image.tag(repository=self._get_repository(app), tag=tag_name)

    def push_image(self, app):
        self.client.images.push(repository=self._get_repository(app))

    def rm(self, app):
        try:
            container = self.client.containers.get(app)
            container.stop()
            container.remove()
        except APIError:
            print('docker.errors.APIError at remove()')

    def pull(self, app):
        self.client.images.pull(self._get_repository(app),
                                auth_config={'username': self.registry_username, 'password': self.registry_password})

    def run(self, app, tag, variables, labels):
        self.client.containers.run(
            image=self._get_repository(app) + f':{tag}',
            labels=labels,
            environment=variables,
            network='plataforma_network',
            ports={"7" + str(randint(100, 999)): 9229},
            name=app,
            detach = True
        )

    def _get_repository(self, app):
        return '{registry}/{app}'.format(registry=self.registry, app=app)
