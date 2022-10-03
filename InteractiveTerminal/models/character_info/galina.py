from ..roll_status import RollStatus
from ..character import Constants
from ...utils import use_passed_or_default

class GalinaNovikova(Constants):
    def __init__(self, **kwargs):
        super().__init__(
            **use_passed_or_default(
                kwargs,
                ICON_SRC="yanfei.png",
                CHARACTER_NAME="Galina Novikova",
                CHARACTER_ROLE="Siren - Section Leader",
                PRONOUN_SHE="she",
                PRONOUN_HER="her",
                PRONOUN_HERS="hers",
                ARMOR_RATING=12,
                ARMOR_BONUS=0,
                SUIT_POWER=3,
                SUIT_CAPACITY=3,
                CURRENT_HP=12,
                MAX_HP=12,
                CURRENT_REVIVES=2,
                MAX_REVIVES=2,
                CURRENT_DEFLECTS=1,
                MAX_DEFLECTS=1,
                CURRENT_HIT_DICE = 2,
                MAX_HIT_DICE = 2,

                CURRENT_DEATH_FAILS = 0,
                MAX_DEATH_FAILS = 2,

                CURRENT_DEATH_SUCCESS = 0,
                MAX_DEATH_SUCCESS = 3,

                S_STRENGTH = -1,
                S_DEXTERITY = 1,
                S_CONSTITUTION = 1,
                S_INTELLIGENCE = 1,
                S_WISDOM = 1,

                S_PROFICIENCY_BONUS = 4,

                P_STR_ATHLETICS = 1,
                P_STR_COMBATIVES = 1,
                P_DEX_ACROBATICS = 0,
                P_DEX_STEALTH = 1,
                P_INT_INVESTIGATION = 0,
                P_INT_NATURE = 1,
                P_INT_ANIMAL_HANDLING = 0,
                P_WIS_INSIGHT = 0,
                P_WIS_MEDICINE = 2,
                P_WIS_PERCEPTION = 0,
                P_WIS_SURVIVAL = 2,
                P_WIS_SOCIAL = 1,

                NEXT_ROLL_STATUS = RollStatus.STANDARD,
            )
        )