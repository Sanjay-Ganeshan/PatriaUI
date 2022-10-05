from kivy.properties import ObjectProperty
from kivymd.uix.boxlayout import MDBoxLayout

from ...new_models.events.ev_base import GameOrViewEvent
from ...new_models.state.app_settings import BOX_WIDTH
from ...new_models.state.state_manager import StateManager
from ..shared.box_sized_mixin import BoxSized
from ..shared.listens_for_state_changes import ListenForStateChanges
from .icon import CHIcon


class CHGeneralInfo(MDBoxLayout, BoxSized, ListenForStateChanges):
    """
    Info needed at a glance
    """

    def __init__(self, **kwargs):
        super().__init__(
            orientation="horizontal",
            box_width=BOX_WIDTH,
            box_height=3,
            **kwargs,
        )
        self.box_init()
        self.listener_init()

        self.icon = CHIcon()
        
        self.add_widget(self.icon)


    def listener(self, ev: GameOrViewEvent, is_forward: bool, state_manager: StateManager) -> None:
        pass
    

