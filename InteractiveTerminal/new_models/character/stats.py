import typing as T
from enum import Enum


class Stat(Enum):
    STRENGTH = "STRENGTH"
    DEXTERITY = "DEXTERITY"
    INTELLIGENCE = "INTELLIGENCE"
    CONSTITUTION = "CONSTITUTION"
    WISDOM = "WISDOM"
    PROFICIENCY_BONUS = "PROFICIENCY"

    @classmethod
    def all(cls) -> T.List["Stat"]:
        return list(cls.__members__.values())
