from commands.platform_base import PlatformBase


class RunApp(PlatformBase):

    def run_presentation(self):
        if self.is_presentation:
            import pdb;pdb.set_trace()
            self.environment.rm(self.get_app())
            self.environment.run(self.get_app_tag(), self.get_app(), self._get_variables(),
                                 dict(self._get_labels(), **self._get_traefik_labels()))

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
