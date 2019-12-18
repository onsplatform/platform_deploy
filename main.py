import argparse

from build_app import BuildApp
from register_app import RegisterApp

parser = argparse.ArgumentParser(description="Deploy na plataforma")
parser.add_argument('--build',
                    help='build a image and push to registry',
                    default=False,
                    action='store_true'
                    )
parser.add_argument('--register_schema',
                    help='build a image and push to registry',
                    default=False,
                    action='store_true'
                    )
parser.add_argument('--platform',
                    help='docker ou openshift',
                    required=True,
                    default='docker'
                    )
parser.add_argument('--environment',
                    help='tst, hmg, prd',
                    required=True,
                    default='tst'
                    )
parser.add_argument('--config_json',
                    help='Arquivo de configuracao (plataforma.json)',
                    default='plataforma.json'
                    )

args = parser.parse_args()

if args.build:
    BuildApp(args).build()
elif args.register_schema:
    RegisterApp(args).register()
