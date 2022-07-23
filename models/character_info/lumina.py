from ..roll_status import RollStatus
from ..character import Constants
from ...utils import use_passed_or_default

class LuminaGale(Constants):
    def __init__(self, **kwargs):
        super().__init__(
            **use_passed_or_default(
                kwargs,
                ICON_SRC="sinon3.png",
                CHARACTER_NAME="Lumina Gale",
                CHARACTER_ROLE="Siren - Sniper",
                PRONOUN_SHE="she",
                PRONOUN_HER="her",
                PRONOUN_HERS="hers",
                ARMOR_RATING=14,
                ARMOR_BONUS=0,
                SUIT_POWER=6,
                SUIT_CAPACITY=6,
                CURRENT_HP=13,
                MAX_HP=13,
                CURRENT_REVIVES=2,
                MAX_REVIVES=2,
                CURRENT_DEFLECTS=2,
                MAX_DEFLECTS=2,
                CURRENT_HIT_DICE = 2,
                MAX_HIT_DICE = 2,

                CURRENT_DEATH_FAILS = 0,
                MAX_DEATH_FAILS = 2,

                CURRENT_DEATH_SUCCESS = 0,
                MAX_DEATH_SUCCESS = 3,

                S_STRENGTH = -1,
                S_DEXTERITY = 1,
                S_CONSTITUTION = 1,
                S_INTELLIGENCE = 2,
                S_WISDOM = 0,

                S_PROFICIENCY_BONUS = 4,

                P_STR_ATHLETICS = 1,
                P_STR_COMBATIVES = 1,
                P_DEX_ACROBATICS = 2,
                P_DEX_STEALTH = 2,
                P_INT_INVESTIGATION = 1,
                P_INT_NATURE = 0,
                P_INT_ANIMAL_HANDLING = 0,
                P_WIS_INSIGHT = 0,
                P_WIS_MEDICINE = 1,
                P_WIS_PERCEPTION = 1,
                P_WIS_SURVIVAL = 0,
                P_WIS_SOCIAL = 0,

                NEXT_ROLL_STATUS = RollStatus.STANDARD,
            )
        )
