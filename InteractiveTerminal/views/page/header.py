from kivymd.uix.boxlayout import MDBoxLayout

from ...new_models.events.ev_base import GameOrViewEvent
from ...new_models.state.app_settings import BOX_WIDTH
from ...new_models.state.state_manager import StateManager
from ..character.general_info import CHGeneralInfo
from ..shared.box_sized_mixin import BoxSized
from ..shared.listens_for_state_changes import ListenForStateChanges


class Header(MDBoxLayout, BoxSized, ListenForStateChanges):
    """
    The info that'll appear at the top, regardless of main content
    """
    def __init__(self, **kwargs):
        super().__init__(
            box_width=BOX_WIDTH,
            box_height=3,
            orientation="vertical",
            **kwargs,
        )
        self.box_init()
        self.listener_init()

        self.general_info = CHGeneralInfo()
        self.add_widget(self.general_info)

    def listener(
        self, ev: GameOrViewEvent, is_forward: bool, state_manager: StateManager
    ) -> None:
        # I don't need to do anything
        pass
