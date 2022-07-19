import typing as T
import dataclasses
from dataclasses import dataclass

@dataclass(frozen=True)
class Constants:
    # General
    ICON_SRC: str = "sinon3.png"
    CHARACTER_NAME: str = "Lumina Gale"
    CHARACTER_ROLE: str = "Siren - Sniper"
    PRONOUN_SHE: str = "she"
    PRONOUN_HER: str = "her"
    PRONOUN_HERS: str = "hers"

    # Armor / Power
    ARMOR_RATING: int = 14
    SUIT_POWER: int = 4
    SUIT_CAPACITY: int = 6
    SHIELD_POWER: int = 2
    SHIELD_CAPACITY: int = 2

    # Life / Death / Avoidance
    CURRENT_HP: int = 13
    MAX_HP: int = 13

    CURRENT_REVIVES: int = 2
    MAX_REVIVES: int = 2

    CURRENT_DEFLECTS: int = 2
    MAX_DEFLECTS: int = 2

    CURRENT_HIT_DICE: int = 2
    MAX_HIT_DICE: int = 2

    CURRENT_DEATH_FAILS: int = 0
    MAX_DEATH_FAILS: int = 2

    CURRENT_DEATH_SUCCESS: int = 0
    MAX_DEATH_SUCCESS: int = 3

    # Stats
    S_STRENGTH: int = -1
    S_DEXTERITY: int = 1
    S_CONSTITUTION: int = 1
    S_INTELLIGENCE: int = 2
    S_WISDOM: int = 0

    # Skills / Proficiencies (0 = normal, 1 = proficient, 2 = expert)
    S_PROFICIENCY_BONUS: int = 4

    # STR
    P_STR_ATHLETICS: int = 1
    P_STR_COMBATIVES: int = 1
    # DEX
    P_DEX_ACROBATICS: int = 2
    P_DEX_STEALTH: int = 2
    # INT
    P_INT_INVESTIGATION: int = 1
    P_INT_NATURE: int = 0
    P_INT_ANIMAL_HANDLING: int = 0
    # WIS
    P_WIS_INSIGHT: int = 0
    P_WIS_MEDICINE: int = 1
    P_WIS_PERCEPTION: int = 1
    P_WIS_SURVIVAL: int = 0
    P_WIS_SOCIAL: int = 0

    @classmethod
    def expand_stat_abbreviation(
        cls,
        three_letters: str,
    ) -> str:
        assert len(three_letters) >= 3, f"Bad: {three_letters}"
        prefix = f"S_{three_letters}"
        for each_field in dataclasses.fields(cls):
            if each_field.name.startswith(prefix):
                return "_".join(each_field.name.split("_")[1:])

        raise IndexError(f"Not found: {three_letters}")

    @classmethod
    def list_skills(cls) -> T.List[str]:
        prefix = "P_"
        return [
            field.name[len(prefix) :]
            for field in dataclasses.fields(cls)
            if field.name.startswith(prefix)
        ]
