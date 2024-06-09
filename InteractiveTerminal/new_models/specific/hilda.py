from ...utils import CircularList, use_passed_or_default
from ..character.character import Character
from ..character.nameplate import Nameplate
from ..character.proficiencies import Proficiency
from ..character.stat_block import StatBlock
from ..character.stats import Stat
from ..character.status import Status

from ..weapons.character_specific_weapons import (
    HildaExperimentalShotgun,
    HildaGrenades,
    HildaJavelin,
    ReplacementSMG,
)

# Jasmine Hayes


class HildaFosse(Character):
    def __init__(self, **kwargs) -> None:
        super().__init__(
            **use_passed_or_default(
                kwargs,
                id_prefix="hilda",
                nameplate=Nameplate(
                    icon="",
                    name="Hilda",
                    surname="Fosse",
                    role="Siren - Sniper",
                    she="she",
                    her="her",
                    hers="hers",
                ),
                stat_block=StatBlock.create(
                    assignments=[
                        (Stat.STRENGTH, 0),
                        (Stat.DEXTERITY, 2),
                        (Stat.CONSTITUTION, 1),
                        (Stat.INTELLIGENCE, 1),
                        (Stat.WISDOM, -1),
                        (Stat.PROFICIENCY_BONUS, 4),
                        (Proficiency.COMBATIVES, 1),
                        (Proficiency.MEDICINE, 1),
                        (Proficiency.ATHLETICS, 1),
                        (Proficiency.ACROBATICS, 2),
                        (Proficiency.STEALTH, 2),
                        (Proficiency.PERCEPTION, 1),
                        (Proficiency.SURVIVAL, 1),
                    ],
                ),
                current_life=None,
                max_life=Status(
                    HP=13,
                    armor_rating=14,
                    revives=2,  # From CON
                    deflects=1,  # From INT
                    hit_dice=2,
                    suit_power=6,
                    shield_power=2,
                    death_fails=2,
                    death_successes=3,
                ),
                weapons=CircularList(
                    items=[
                        HildaExperimentalShotgun(),
                        HildaJavelin(),
                        HildaGrenades(),
                        ReplacementSMG(),
                    ]
                ),
            )
        )
