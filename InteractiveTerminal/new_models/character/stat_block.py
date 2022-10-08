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
    stat_modifiers: T.Dict[str, int] = field(default_factory=dict)
    proficiency_multipliers: T.Dict[str, int] = field(default_factory=dict)

    def __getitem__(self, key: T.Union[Stat, Proficiency]) -> int:
        assert isinstance(key, (Stat, Proficiency)), f"Weird key: {key}"

        if isinstance(key, Stat):
            return self.stat_modifiers.get(key.value, 0)
        if isinstance(key, Proficiency):
            return self.proficiency_multipliers.get(key.value, 0)

    @classmethod
    def create(
        cls, assignments: T.List[T.Tuple[T.Union[Stat, Proficiency], int]]
    ) -> "StatBlock":
        stat_modifiers = {}
        proficiency_multipliers = {}

        for (key, val) in assignments:
            assert isinstance(key, (Stat, Proficiency)), f"Weird key: {key}"
            assert isinstance(val, int), f"Weird value: {val}"

            if isinstance(key, Stat):
                stat_modifiers[key.value] = val
            else:
                proficiency_multipliers[key.value] = val

        return cls(
            stat_modifiers=stat_modifiers,
            proficiency_multipliers=proficiency_multipliers,
        )

    def copy(
        self,
        assignments: T.List[T.Tuple[T.Union[Stat, Proficiency], int]] = None
    ) -> "StatBlock":
        if assignments is None:
            assignments = []

        desired = StatBlock.create(assignments=assignments)

        proficiency_multipliers = {}
        stat_modifiers = {}

        stat_modifiers.update(self.stat_modifiers)
        stat_modifiers.update(desired.stat_modifiers)

        proficiency_multipliers.update(self.proficiency_multipliers)
        proficiency_multipliers.update(desired.proficiency_multipliers)

        return StatBlock(
            stat_modifiers=stat_modifiers,
            proficiency_multipliers=proficiency_multipliers,
        )
