from ...utils import CircularList, use_passed_or_default
from ..character.character import Character
from ..character.nameplate import Nameplate
from ..character.active_effects import Debuffs
from ..character.proficiencies import Proficiency
from ..character.stat_block import StatBlock
from ..character.stats import Stat
from ..character.status import Status
from ..weapons.character_specific_weapons import (
    ZoeLSW,
    ZoePistol,
    ZoeGrenades,
    ReplacementSMG,
    Knife
)


class ZoeSparks(Character):
    def __init__(self, **kwargs) -> None:
        super().__init__(
            **use_passed_or_default(
                kwargs,
                id_prefix="zoe",
                nameplate=Nameplate(
                    icon="zoe.png",
                    name="Zoe",
                    surname="Sparks",
                    role="Siren - Spotter",
                    she="she",
                    her="her",
                    hers="hers",
                ),
                stat_block=StatBlock.create(
                    assignments=[
                        (Stat.STRENGTH, -1),
                        (Stat.DEXTERITY, 1),
                        (Stat.CONSTITUTION, 1),
                        (Stat.INTELLIGENCE, 2),
                        (Stat.WISDOM, 0),
                        (Stat.PROFICIENCY_BONUS, 4),
                        (Proficiency.COMBATIVES, 1),
                        (Proficiency.MEDICINE, 1),
                        (Proficiency.INVESTIGATION, 1),
                        (Proficiency.PERCEPTION, 1),
                        (Proficiency.STEALTH, 1),
                        (Proficiency.ACROBATICS, 1),
                        (Proficiency.ATHLETICS, 1),
                    ],
                ),
                current_life=None,
                max_life=Status(
                    HP=13, # 12 + CON
                    armor_rating=14,
                    revives=2,  # From CON (-1 for autoraise)
                    deflects=2,  # From INT
                    hit_dice=2,
                    suit_power=6,
                    shield_power=2,
                    death_fails=2,
                    death_successes=3,
                ),
                weapons=CircularList(
                    items=[
                        ZoeLSW(),
                        ZoePistol(),
                        ZoeGrenades(),
                        ReplacementSMG(),
                        Knife(),
                        ]
                ),
                active_effects = []
            )
        )
