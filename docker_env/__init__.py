import docker

from docker.errors import APIError
from random import randint


class DockerAppDeploy:

    def __init__(self, config):
        self.config = config
        self.client = docker.from_env()

    def deploy(self, image_id):
        variables = {
            'API_MODE': True,
            'SYSTEM_ID': self.config['solution']['id']
        }
        if self.config['app']['type'] == 'presentation':
            self.rm()
            self.run(image_id, variables)

    def build_image(self):
        build = self.client.images.build(path='.', tag=self._get_tag(), labels=self._get_labels(), nocache=True)
        if build:
            return build[0]

    def rm(self):
        docker_name = self.config['app']['docker']
        try:
            container = self.client.containers.get(docker_name)
            container.remove()
        except APIError:
            print('docker.errors.APIError at remove()')

    def run(self, image, variables):
        debug_port = "7" + str(randint(100, 999))
        docker_name = self.config['app']['docker']
        default_labels = self._get_labels()
        traefik_labels = self._get_traefik_labels()

        self.client.containers.run(
            image=image,
            labels=dict(default_labels, **traefik_labels),
            environment=variables,
            network='plataforma_network',
            ports={debug_port: 9229},
            name=docker_name
        )

    def _get_labels(self):
        return {
            'app_name': self.config['app']['docker'],
            'system_id': self.config['solution']['id'],
            'process_id': self.config['app']['id']
        }

    def _get_traefik_labels(self):
        docker_name = self.config['app']['docker']
        return {
            'traefik.backend': docker_name,
            'traefik.' + docker_name + '.frontend.rule': 'PathPrefixStrip: /' + docker_name,
            'traefik.docker.network': 'plataforma_network',
            'traefik.port': '8088'
        }

    def _get_tag(self):
        version = self.config['app']['version']
        docker_name = self.config['app']['docker']
        return 'registry:5000/{docker_name}:{version}'.format(docker_name=docker_name, version=version)
