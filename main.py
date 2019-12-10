import argparse

from datetime import datetime

from deploy_app import DeployApp


def valid_date(s):
    try:
        return datetime.strptime(s, "%d/%m/%Y")
    except ValueError:
        msg = "Not a valid date: '{0}'.".format(s)
        raise argparse.ArgumentTypeError(msg)


parser = argparse.ArgumentParser(description="Deploy na plataforma")
parser.add_argument('--date_begin_validity',
                    help='Inicio de vigência da aplicação',
                    required=False,
                    type=valid_date
                    )
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
