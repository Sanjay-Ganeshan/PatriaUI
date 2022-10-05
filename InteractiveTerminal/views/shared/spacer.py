from kivy.uix.widget import Widget

from .box_sized_mixin import BoxSized


class Spacer(BoxSized, Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.box_init()
