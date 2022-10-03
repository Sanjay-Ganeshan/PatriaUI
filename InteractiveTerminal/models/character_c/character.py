from dataclasses import dataclass, field
import typing as T

from .stat_block import StatBlock
from .nameplate import Nameplate
from .status import Status


# NOT frozen

@dataclass
class Character:
    """
    Stores all relevant information about a character
    """
    nameplate: Nameplate = field(default_factory=Nameplate)
    stat_block: StatBlock = field(default_factory=StatBlock)

    current_life: Status = field(default_factory=Status)
    max_life: Status = field(default_factory=Status)

    active_effects: T.List[str] = field(default_factory=list)

    






