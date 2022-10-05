# The main page, regardless of contents
from kivy.properties import ObjectProperty
from kivymd.uix.boxlayout import MDBoxLayout

from ...new_models.state.app_settings import BOX_WIDTH
from ..shared.box_sized_mixin import BoxSized


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
