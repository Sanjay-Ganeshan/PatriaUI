from ...new_models.state.state_manager import StateManager
from ..powerful_json import dumps

from ...new_models.specific.lumina import LuminaGale
from ...new_models.specific.galina import GalinaNovikova
from ...new_models.specific.silvia import SilviaFerreyra

from ...new_models.state.view_state import Views
from ...new_models.events.view_events import SwitchFocusedCharacter, SwitchFocusedView

import unittest


class TestCanSaveStateManager(unittest.TestCase):
    def test_save_state_manager(self) -> None:
        state_manager = StateManager()
        state_manager.game_state.characters["lumina"] = LuminaGale()
        state_manager.game_state.characters["galina"] = GalinaNovikova()
        state_manager.game_state.characters["silvia"] = SilviaFerreyra()
        state_manager.push_event(
            SwitchFocusedView(new_focus=Views.CHARACTER_DETAILS)
        )
        state_manager.push_event(SwitchFocusedCharacter(new_focus="lumina"))
        state_manager.clear_history()
        dumps(state_manager, indent=2)
