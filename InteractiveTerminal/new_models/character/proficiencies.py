import typing as T
from enum import Enum, unique

from .stats import Stat

@unique
class Proficiency(Enum):
    # STR
    ATHLETICS = "ATHLETICS" 
    COMBATIVES = "COMBATIVES" 
    # DEX
    ACROBATICS = "ACROBATICS" 
    STEALTH = "STEALTH" 
    # INT
    INVESTIGATION = "INVESTIGATION" 
    NATURE = "NATURE" 
    ANIMAL_HANDLING = "ANIMAL_HANDLING" 
    # WIS
    INSIGHT = "INSIGHT" 
    MEDICINE = "MEDICINE" 
    PERCEPTION = "PERCEPTION" 
    SURVIVAL = "SURVIVAL" 
    SOCIAL = "SOCIAL"

    def corresponding_stat(self) -> Stat:
        return {
            # STR
            Proficiency.ATHLETICS: Stat.STRENGTH,
            Proficiency.COMBATIVES: Stat.STRENGTH,
            # DEX
            Proficiency.ACROBATICS: Stat.DEXTERITY,
            Proficiency.STEALTH: Stat.DEXTERITY,
            # INT
            Proficiency.INVESTIGATION: Stat.INTELLIGENCE,
            Proficiency.NATURE: Stat.INTELLIGENCE,
            Proficiency.ANIMAL_HANDLING: Stat.INTELLIGENCE,
            # WIS
            Proficiency.INSIGHT: Stat.WISDOM,
            Proficiency.MEDICINE: Stat.WISDOM,
            Proficiency.PERCEPTION: Stat.WISDOM,
            Proficiency.SURVIVAL: Stat.WISDOM,
            Proficiency.SOCIAL: Stat.WISDOM,
        }[self]

    @classmethod
    def all(cls) -> T.List["Proficiency"]:
        return list(Proficiency.__members__.values())
