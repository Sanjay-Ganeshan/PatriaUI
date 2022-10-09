import unittest
import json

from ..api import (
    get_other_player_events,
    send_events,
    delete_event,
    save_backup,
    get_backup,
    delete_backup,
)
from ...save.powerful_json import dumps, loads
from ...new_models.state.state_manager import StateManager
from ...new_models.events.game_events import ChangeWeapons

class TestNetworkAPI(unittest.TestCase):
    def test_get(self) -> None:
        views = get_other_player_events("sana")
        print(views)

    def test_send(self) -> None:
        # send_events(ChangeWeapons(character_id="lumina"))
        pass

    def test_delete(self) -> None:
        # delete_event("sanga__5433150")
        pass

    def test_save_backup(self) -> None:
        state_manager_dump = dumps(StateManager())
        self.assertTrue(save_backup(state_manager_dump, "fake_user"))
        backup = get_backup("fake_user")
        self.assertIsNotNone(backup)
        self.assertIsInstance(backup, StateManager)
