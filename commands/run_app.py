from commands.platform_base import PlatformBase


class RunApp(PlatformBase):

    def run_presentation(self):
        if self.is_presentation:
            container_name = self.get_app()
            if self.environment.container_exists(container_name):
                self.environment.rm(container_name)
                print('Previous container removed')

            self.environment.pull(container_name)
            print('Pulled image')

            print('Staterd Run docker container process')
            self.environment.run(container_name, self.get_tag_name(), self._get_variables(),
                                 dict(self._get_labels(), **self._get_traefik_labels()))
            print('Container is up and running!')
            
    def _get_variables(self):
        return {
            'API_MODE': True,
            'SYSTEM_ID': self.get_system_id(),
            'PROCESS_ID': self.get_app_process_id()
        }

    def _get_traefik_labels(self):
        return {
            'traefik.backend': self.get_app(),
            'traefik.' + self.get_app() + '.frontend.rule': 'PathPrefixStrip: /' + self.get_app(),
            'traefik.docker.network': 'plataforma_network',
            'traefik.port': '8088'
        }
