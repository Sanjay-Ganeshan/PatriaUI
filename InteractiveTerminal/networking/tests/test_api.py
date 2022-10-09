import unittest

from ..api import get_other_player_events, send_event, delete_event
from ...new_models.events.game_events import ChangeWeapons

class TestNetworkAPI(unittest.TestCase):
    def test_get(self) -> None:
        views = get_other_player_events("sana")
        print(views)

    def test_send(self) -> None:
        # send_event(ChangeWeapons(character_id="lumina"))
        pass

    def test_delete(self) -> None:
        # delete_event("sanga__5433150")
        pass
