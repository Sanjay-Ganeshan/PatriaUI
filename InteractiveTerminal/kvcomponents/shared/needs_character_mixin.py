from ...models.character import Constants
from ...models.help_text import HelpText
from kivy.properties import ObjectProperty


class NeedsConstants:
    constants: Constants = ObjectProperty(None)
    help_text: HelpText = ObjectProperty(HelpText(Constants()))

    def adapt_to_constants(self, *args):
        self.help_text = HelpText(self.constants)
        to_update = []
        if hasattr(self, "children"):
            for each_child in self.children:
                if isinstance(each_child, NeedsConstants):
                    to_update.append(each_child)
        for each_attr in dir(self):
            possible_child = getattr(self, each_attr)
            if (
                isinstance(possible_child, NeedsConstants)
                and possible_child not in to_update
            ):
                to_update.append(possible_child)

        for each_update in to_update:
            each_update.constants = self.constants

    def constants_init(self):
        self.bind(constants=self.adapt_to_constants)
