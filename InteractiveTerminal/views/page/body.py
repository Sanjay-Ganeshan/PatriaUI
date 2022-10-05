# The main page, regardless of contents
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.properties import ObjectProperty

from ..shared.box_sized_mixin import BoxSized
from ..shared.spacer import Spacer
from ...new_models.state.app_settings import BOX_WIDTH

from ...new_models.state.view_state import ViewState, Views

class Body(MDBoxLayout, BoxSized):
    """
    A container for the main content we want to display
    """
    which_view: Views = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(
            box_width=BOX_WIDTH,
            box_height=10,
            orientation="vertical",
            **kwargs,
        )
        self.box_init()

        self.content = Spacer(box_width=BOX_WIDTH, box_height=10)

        self.bind(which_view=self.update_which_view)

    def update_which_view(self, *args):
        self.remove_widget(self.content)
        
        if self.which_view is None or self.which_view == Views.EMPTY:
            self.content = Spacer(box_width=BOX_WIDTH, box_height=10)

        elif self.which_view == Views.CHARACTER_DETAILS:
            pass

        elif self.which_view == Views.MAP:
            pass

