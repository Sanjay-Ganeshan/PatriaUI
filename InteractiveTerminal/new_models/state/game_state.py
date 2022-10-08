import typing as T
from dataclasses import dataclass, field

from ..character.character import Character
from ..map.maps import Map



@dataclass
class GameState:
    """
    Authoritative state of the game
    """

    characters: T.Dict[str, Character] = field(default_factory=dict)
    the_map: Map = field(default_factory=Map)
    chat_log: T.List[str] = field(default_factory=list)
