import argparse

from commands.run_app import RunApp
from commands.build_app import BuildApp
from commands.register_app import RegisterApp

parser = argparse.ArgumentParser(description="Deploy na plataforma")
parser.add_argument('--build',
                    help='compila uma imagem e envia para o registro de imagens',
                    default=False,
                    action='store_true'
                    )
parser.add_argument('--register_schema',
                    help='registra uma aplicação no schema do ambiente',
                    default=False,
                    action='store_true'
                    )
parser.add_argument('--run_presentation',
                    help='inicia uma aplicação do tipo presenter',
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
                    help='arquivo de configuração (plataforma.json)',
                    default='plataforma.json'
                    )

args = parser.parse_args()

if args.build:
    BuildApp(args).build()
elif args.register_schema:
    RegisterApp(args).register()
elif args.run_presentation:
    RunApp(args).run_presentation()
