# The main page, regardless of contents
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.properties import ObjectProperty

from ..shared.box_sized_mixin import BoxSized
from ...new_models.state.app_settings import BOX_WIDTH

class Footer(MDBoxLayout, BoxSized):
    """
    The info that'll appear at the bottom, regardless of main content
    """
    def __init__(self, **kwargs):
        super().__init__(
            box_width=BOX_WIDTH,
            box_height=3,
            orientation="vertical",
            **kwargs,
        )
        self.box_init()
