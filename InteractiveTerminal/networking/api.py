import requests
from ..utils import get_username

from ..new_models.events.ev_base import GameOrViewEvent
from ..save.powerful_json import loads, dumps
import json

import typing as T


URL = "https://ynr5oe4g3f.execute-api.us-east-2.amazonaws.com/default/PatriaREST"

def get_other_player_events(my_username: T.Optional[str] = None) -> T.List[GameOrViewEvent]:
    if my_username is None:
        my_username=get_username()

    resp = requests.get(
        URL,
        params = {
            "username": my_username,
        },
    )

    if resp.status_code == 200:
        loaded_obj = loads(resp.content)
        assert isinstance(loaded_obj, list), f"Bad: {loaded_obj}"
        
        results = []
        for each_ev in loaded_obj:
            if isinstance(each_ev, GameOrViewEvent):
                results.append(each_ev)
            else:
                pass
        
        return results

    else:
        return []


def send_event(ev: GameOrViewEvent) -> None:
    dumped = dumps(ev)
    
    response = requests.put(
        URL,
        json=json.loads(dumped),
    )


def delete_event(event_id: str) -> None:
    response = requests.delete(
        URL,
        json={"event_id": event_id},
    )

