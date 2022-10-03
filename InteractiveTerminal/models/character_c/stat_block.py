import typing as T
from dataclasses import dataclass, field

from .proficiencies import Proficiency
from .stats import Stat

@dataclass(frozen=True)
class StatBlock:
    """
    Tracks how good a character is at particular
    stats and skills
    """
    proficiency_bonus: int = 4
    stat_modifiers: T.Dict[Stat, int] = field(default_factory=dict)
    proficiency_multipliers: T.Dict[Proficiency, int] = field(default_factory=dict)

    def __getitem__(self, key: T.Union[Stat, Proficiency]) -> int:
        assert isinstance(key, (Stat, Proficiency)), f"Weird key: {key}"

        if isinstance(key, Stat):
            return self.stat_modifiers.get(key, 0)
        if isinstance(key, Proficiency):
            return self.proficiency_multipliers.get(key, 0)
    
    @classmethod
    def create(
        cls,
        proficiency_bonus: int,
        *assignments: T.Tuple[T.Union[Stat, Proficiency], int]
    ) -> "StatBlock":
        stat_modifiers = {}
        proficiency_multipliers = {}

        for (key, val) in assignments:
            assert isinstance(key, (Stat, Proficiency)), f"Weird key: {key}"
            assert isinstance(val, int), f"Weird value: {val}"

            if isinstance(key, Stat):
                stat_modifiers[key] = val
            else:
                proficiency_multipliers[key] = val

        return cls(
            proficiency_bonus=proficiency_bonus,
            stat_modifiers=stat_modifiers,
            proficiency_multipliers=proficiency_multipliers,
        )
    
    def copy(
        self,
        proficiency_bonus: T.Optional[int] = None,
        *assignments: T.Tuple[T.Union[Stat, Proficiency], int]
    ) -> "StatBlock":
        if proficiency_bonus is None:
            proficiency_bonus = self.proficiency_bonus
        
        desired = StatBlock.create(0, *assignments)
        
        proficiency_multipliers = {}
        stat_modifiers = {}
        
        stat_modifiers.update(self.stat_modifiers)
        stat_modifiers.update(desired.stat_modifiers)

        proficiency_multipliers.update(self.proficiency_multipliers)
        proficiency_multipliers.update(desired.proficiency_multipliers)

        return StatBlock(
            proficiency_bonus=proficiency_bonus,
            stat_modifiers=stat_modifiers,
            proficiency_multipliers=proficiency_multipliers,
        )