from enum import Enum
import typing as T

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