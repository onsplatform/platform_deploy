import argparse

from deploy_app import DeployApp


parser = argparse.ArgumentParser(description="Deploy na plataforma")
parser.add_argument('--environment',
                    help='docker ou openshift',
                    required=True,
                    default='docker'
                    )
parser.add_argument('--config_json',
                    help='Arquivo de configuracao (plataforma.json)',
                    default='plataforma.json'
                    )

args = parser.parse_args()

deploy_app = DeployApp()
deploy_app.register_app(args)
