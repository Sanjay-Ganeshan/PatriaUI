import typing as T
from dataclasses import dataclass, field

from ..dice.advantage import RollStatus
from .active_effects import Buffs, Debuffs
from .nameplate import Nameplate
from .stat_block import StatBlock
from .status import Status

# NOT frozen

@dataclass
class Character:
    """
    Stores all relevant information about a character
    """
    # An ID that will be used by this character. If there are
    # multiple of this character, we'll use this as the prefix,
    # but will add a number (like lumina-2)
    id_prefix: str = field(default_factory="ch_id")

    nameplate: Nameplate = field(default_factory=Nameplate)
    stat_block: StatBlock = field(default_factory=StatBlock)

    current_life: Status = field(default=None)
    max_life: Status = field(default_factory=Status)

    active_effects: T.List[str] = field(default_factory=list)
    next_roll_status: RollStatus = RollStatus.STANDARD

    def __post_init__(self):
        if self.current_life is None:
            self.current_life = self.max_life

    def add_effect(self, effect: T.Union[str, Buffs, Debuffs]) -> None:
        if isinstance(effect, (Buffs, Debuffs)):
            effect = effect.value

        if effect not in self.active_effects:
            self.active_effects.append(effect)

    def remove_effect(self, effect: T.Union[str, Buffs, Debuffs]) -> None:
        if isinstance(effect, (Buffs, Debuffs)):
            effect = effect.value

        if effect in self.active_effects:
            self.active_effects.remove(effect)

    def has_effect(self, effect: T.Union[str, Buffs, Debuffs]) -> bool:
        if isinstance(effect, (Buffs, Debuffs)):
            effect = effect.value

        return effect in self.active_effects
    
        

    






