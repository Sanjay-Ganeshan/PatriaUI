# The main page, regardless of contents
from kivy.properties import ObjectProperty
from kivymd.uix.boxlayout import MDBoxLayout

from ...new_models.state.app_settings import BOX_WIDTH
from ...new_models.state.view_state import Views, ViewState
from ..shared.box_sized_mixin import BoxSized
from ..shared.spacer import Spacer
from ..shared.listens_for_state_changes import ListenForStateChanges
from .details import DetailsSheet
from ...new_models.events.ev_base import GameOrViewEvent
from ...new_models.events.view_events import SwitchFocusedView
from ...new_models.state.state_manager import StateManager


class Body(MDBoxLayout, BoxSized, ListenForStateChanges):
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
        self.listener_init()


        self.empty = Spacer(box_width=BOX_WIDTH, box_height=10)
        self.details = DetailsSheet()
        self.content = self.empty

        self.bind(which_view=self.update_which_view)

    def update_which_view(self, *args):
        self.remove_widget(self.content)
        
        if self.which_view is None or self.which_view == Views.EMPTY:
            self.content = self.empty

        elif self.which_view == Views.CHARACTER_DETAILS:
            self.content = self.details

        elif self.which_view == Views.MAP:
            pass
    
        self.add_widget(self.content)


    def listener(
        self, ev: GameOrViewEvent, is_forward: bool, state_manager: StateManager
    ) -> None:
        if not isinstance(ev, SwitchFocusedView):
            return

        self.which_view = state_manager.view_state.focused_view
        

