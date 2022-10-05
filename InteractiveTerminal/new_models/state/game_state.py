from dataclasses import dataclass, field

import typing as T

from ..character.character import Character

@dataclass
class GameState:
    """
    Authoritative state of the game
    """

    characters: T.Dict[str, Character] = field(default_factory=dict)