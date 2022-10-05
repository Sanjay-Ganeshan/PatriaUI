from kivy.properties import NumericProperty
from kivymd.uix.boxlayout import MDBoxLayout


class BoxSized:
    box_width = NumericProperty(1)
    box_height = NumericProperty(1)

    def box_init(self):
        self.bind(parent=self.set_size)

    def set_size(self, *args) -> None:
        if self.parent is not None and isinstance(self.parent, BoxSized):
            self.size_hint = (
                self.box_width / self.parent.box_width,
                self.box_height / self.parent.box_height,
            )



class BoxSizedBoxLayout(MDBoxLayout, BoxSized):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.box_init()
