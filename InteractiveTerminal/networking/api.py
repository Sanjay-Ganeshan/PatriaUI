import requests
from ..utils import get_username

from ..new_models.events.ev_base import GameOrViewEvent
from ..save.powerful_json import loads, dumps
import json
import os

import typing as T


BASE_URL = "https://ynr5oe4g3f.execute-api.us-east-2.amazonaws.com/default"
EVENT_ENDPOINT = f"{BASE_URL}/events"
BACKUP_ENDPOINT = f"{BASE_URL}/backup"
IMAGES_ENDPOINT = f"{BASE_URL}/images"

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

def download_image(remote_name: str, destination_dir: str) -> bool:
    # The server gives us credentials to log into S3
    remote_name = os.path.basename(remote_name)
    assert remote_name.endswith(".png"), f"{remote_name} should end with .png"
    presigned_url = _generate_presigned_image_url(remote_name, "get")
    if presigned_url is None:
        return False
    else:
        response = requests.get(presigned_url, stream=True)
        if response.status_code != 200:
            return False
        else:
            destination_dir = os.path.abspath(destination_dir)
            if not os.path.exists(destination_dir):
                os.makedirs(destination_dir, exist_ok=True)
            with open(os.path.join(destination_dir, remote_name), "wb") as f:
                for chunk in response.iter_content(4096):
                    f.write(chunk)
            return True

def upload_image(image_path: str) -> bool:
    image_path = os.path.abspath(image_path)
    remote_name = os.path.basename(image_path)
    assert remote_name.endswith(".png"), f"{image_path} should end with .png"

    with open(image_path, "rb") as f:
        data = f.read()

    presigned_url = _generate_presigned_image_url(remote_name, "put")
    if presigned_url is None:
        return False
    else:
        response = requests.put(presigned_url, data=data)

        return response.status_code == 200

def _generate_presigned_image_url(img: str, operation: str) -> T.Optional[str]:
    operation = operation.lower().strip()
    assert operation in ["get", "put", "delete"], f"Bad operation: {operation}"
    
    fn = getattr(requests, operation)
    resp = fn(
        IMAGES_ENDPOINT,
        params = {
            "img": img,
            # Ultra basic security to prevent easy scraping.
            "salt": os.path.basename(__file__),
        },
    )

    if resp.status_code == 200:
        loaded_obj = loads(resp.content)
        return loaded_obj

    else:
        print(resp.content)
        return None
