import json


class PlatformBase:

    def __init__(self, args):
        self.load_platform_json(args)

    def load_platform_json(self, args):
        with open(args.config_json) as json_file:
            self.platform_json = json.load(json_file)

    def get_tag_name(self):
        return self.platform_json['app']['version']

    def get_app_tag(self):
        return '{app}:{tag}'.format(app=self.get_app(), tag=self.get_tag_name())

    def get_app(self):
        return self.platform_json['app']['container']
