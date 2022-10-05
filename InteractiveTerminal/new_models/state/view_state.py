# All settings that have to do with the UI (i.e. what
# screen am I looking at?) that don't have to do with the game
# itself

import typing as T
from dataclasses import dataclass, field
from enum import Enum, unique

@unique
class Views(Enum):
    """
    Controls the center of the page
    """
    # Blank canvas
    EMPTY = "EMPTY"
    
    # Stats, skills, and abilities
    CHARACTER_DETAILS = "CHARACTER_DETAILS"

    # Where things are on the map
    MAP = "MAP"



@dataclass
class ViewState:
    focused_view: Views = Views.EMPTY
    focused_character: T.Optional[str] = None
