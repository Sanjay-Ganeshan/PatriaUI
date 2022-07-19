from .box_sized_mixin import BoxSized
from .tooltip import OptionalTooltip
from kivymd.uix.label import MDLabel

class CenteredLabel(MDLabel, BoxSized, OptionalTooltip):
    def __init__(self, **kwargs):
        super().__init__(
            halign=kwargs.pop("halign", "center"),
            valign=kwargs.pop("valign", "middle"),
            font_style=kwargs.pop("font_style", "H4"),
            **kwargs,
        )
        self.box_init()

        self.bind(size=self.change_text_size)

    def change_text_size(self, *args):
        self.text_size = self.size
