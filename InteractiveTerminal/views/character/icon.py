from kivy.properties import StringProperty
from kivy.uix.image import Image

from ...new_models.events.ev_base import GameOrViewEvent
from ...new_models.events.view_events import SwitchFocusedCharacter
from ...new_models.state.state_manager import StateManager
from ..shared.box_sized_mixin import BoxSized
from ..shared.listens_for_state_changes import ListenForStateChanges
from ..shared.touchable_mixin import TouchableMixin


class CHIcon(Image, BoxSized, TouchableMixin, ListenForStateChanges):
    icon_src: str = StringProperty("missing.png")

    def __init__(self, **kwargs):
        super().__init__(
            source="missing.png",
            box_width=1,
            box_height=3,
            allow_stretch=True,
            **kwargs,
        )
        self.box_init()
        self.touch_init()
        self.listener_init()

        self.bind(icon_src=self.icon_src_updated)

    def icon_src_updated(self, *args):
        self.source = self.icon_src

    def on_left_click(self, position):
        # change characters
        if self.state_manager is not None:
            chars = sorted(self.state_manager.game_state.characters.keys())
            my_idx = -1 if self.state_manager.view_state.focused_character is None else chars.index(self.state_manager.view_state.focused_character)
            next_char = chars[(my_idx + 1) % len(chars)]
            self.state_manager.push_event(
                SwitchFocusedCharacter(
                    new_focus=next_char,
                )
            )


    def listener(self, ev: GameOrViewEvent, is_forward: bool, state_manager: StateManager) -> None:
        if not isinstance(ev, SwitchFocusedCharacter):
            return

        # We might have changed the current character's icon. Look it up
        if state_manager.view_state.focused_character is None:
            self.icon_src = "missing.png"
        else:
            self.icon_src = state_manager.game_state.characters[state_manager.view_state.focused_character].nameplate.icon
