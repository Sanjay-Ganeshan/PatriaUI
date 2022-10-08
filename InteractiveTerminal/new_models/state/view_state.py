# All settings that have to do with the UI (i.e. what
# screen am I looking at?) that don't have to do with the game
# itself

import typing as T
from dataclasses import dataclass
from enum import Enum, unique


@unique
class Views(Enum):
    """
    Controls the center of the page
    """
    # Stats, skills, and abilities
    CHARACTER_DETAILS = "CHARACTER_DETAILS"

    # Where things are on the map
    MAP = "MAP"

    def next(self) -> "Views":
        if self == Views.CHARACTER_DETAILS:
            return Views.MAP
        else:
            return Views.CHARACTER_DETAILS



@dataclass
class ViewState:
    focused_view: Views = Views.CHARACTER_DETAILS
    focused_character: T.Optional[str] = None
    chat_log_index: int = -1
