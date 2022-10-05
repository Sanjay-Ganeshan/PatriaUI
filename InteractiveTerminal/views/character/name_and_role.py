from kivy.properties import StringProperty

from ...new_models.character.character import Character
from ...new_models.events.ev_base import GameOrViewEvent
from ...new_models.events.view_events import SwitchFocusedCharacter
from ...new_models.state.state_manager import StateManager
from ..shared.centered_label import CenteredLabel
from ..shared.listens_for_state_changes import ListenForStateChanges


class CHNamecard(CenteredLabel, ListenForStateChanges):
    character_name: str = StringProperty("<name>")
    character_role: str = StringProperty("<role>")

    def __init__(self, **kwargs):
        super().__init__(
            text="",
            box_width=1.5,
            box_height=3,
            font_style="H5",
            **kwargs,
        )
        self.box_init()
        self.listener_init()

        self.bind(character_name=self.update_text, character_role=self.update_text)

    def update_text(self, *args):
        self.text = f"{self.character_name}\n{self.character_role}"

    def listener(self, ev: GameOrViewEvent, is_forward: bool, state_manager: StateManager) -> None:
        if not isinstance(ev, SwitchFocusedCharacter):
            return

        # We might have changed the current character's icon. Look it up
        if state_manager.view_state.focused_character is None:
            self.character_name = "<name>"
            self.character_role = "<role>"
        else:
            ch: Character = state_manager.game_state.characters[state_manager.view_state.focused_character]
            self.character_name = ch.nameplate.name
            self.character_role = ch.nameplate.role
