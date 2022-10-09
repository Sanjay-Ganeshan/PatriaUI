import requests
from ..utils import get_username

from ..new_models.events.ev_base import GameOrViewEvent
from ..save.powerful_json import loads, dumps
import json

import typing as T


BASE_URL = "https://ynr5oe4g3f.execute-api.us-east-2.amazonaws.com/default"
EVENT_ENDPOINT = f"{BASE_URL}/events"
BACKUP_ENDPOINT = f"{BASE_URL}/backup"

def get_other_player_events(my_username: T.Optional[str] = None) -> T.List[GameOrViewEvent]:
    if my_username is None:
        my_username=get_username()

    resp = requests.get(
        EVENT_ENDPOINT,
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


def send_events(evs: T.List[GameOrViewEvent]) -> None:
    dumped = dumps(evs)
    
    response = requests.put(
        EVENT_ENDPOINT,
        json=json.loads(dumped),
    )


def delete_event(event_id: str) -> None:
    response = requests.delete(
        EVENT_ENDPOINT,
        json={"event_id": event_id},
    )


def get_backup(my_username: T.Optional[str] = None) -> T.Optional[T.Any]:
    if my_username is None:
        my_username=get_username()

    resp = requests.get(
        BACKUP_ENDPOINT,
        params = {
            "username": my_username,
        },
    )

    if resp.status_code == 200:
        loaded_obj = loads(resp.content)
        return loaded_obj

    else:
        return None


def save_backup(state_manager_dump: str, my_username: T.Optional[str] = None) -> bool:
    if my_username is None:
        my_username=get_username()

    resp = requests.put(
        BACKUP_ENDPOINT,
        params={
            "username": my_username,
        },
        json=json.loads(state_manager_dump)
    )

    if resp.status_code == 200:
        return True
    else:
        print(resp.content)
        return False

def delete_backup(my_username: T.Optional[str] = None) -> bool:
    if my_username is None:
        my_username=get_username()

    resp = requests.delete(
        BACKUP_ENDPOINT,
        params={
            "username": my_username,
        },
    )

    if resp.status_code == 200:
        return True
    else:
        return False
