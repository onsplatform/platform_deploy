from commands.platform_base import PlatformBase


class BuildApp(PlatformBase):

    def __init__(self, args):
        super().__init__(args)

    def build(self):
        image = self.environment.build_image(self.get_app_and_tag(), self._get_labels())
        if image and self.environment.tag(image, self.get_tag_name(), self.get_app()):
            self.environment.push_image(self.get_app())
