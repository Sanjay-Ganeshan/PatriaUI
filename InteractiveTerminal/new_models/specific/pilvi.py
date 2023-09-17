from ...utils import CircularList, use_passed_or_default
from ..character.character import Character
from ..character.nameplate import Nameplate
from ..character.proficiencies import Proficiency
from ..character.stat_block import StatBlock
from ..character.stats import Stat
from ..character.status import Status
from ..weapons.character_specific_weapons import (
    PilviBR,
    PilviGrenadeLauncher,
    PilviGrenades,
    PilviPistol,
    ReplacementSMG,
)


class PilviKoppel(Character):
    def __init__(self, **kwargs) -> None:
        super().__init__(
            **use_passed_or_default(
                kwargs,
                id_prefix="pilvi",
                nameplate=Nameplate(
                    icon="pilvi.png",
                    name="Pilvi",
                    surname="Koppel",
                    role="Siren - Spotter",
                    she="she",
                    her="her",
                    hers="hers",
                ),
                stat_block=StatBlock.create(
                    assignments=[
                        (Stat.STRENGTH, -1),
                        (Stat.DEXTERITY, 0),
                        (Stat.CONSTITUTION, 2),
                        (Stat.INTELLIGENCE, 1),
                        (Stat.WISDOM, 1),
                        (Stat.PROFICIENCY_BONUS, 4),
                        (Proficiency.COMBATIVES, 1),
                        (Proficiency.MEDICINE, 2),
                        (Proficiency.PERCEPTION, 2),
                        (Proficiency.INVESTIGATION, 1),
                        (Proficiency.SOCIAL, 1),
                        (Proficiency.NATURE, 1),
                    ],
                ),
                current_life=None,
                max_life=Status(
                    HP=14,
                    armor_rating=14,
                    revives=3,  # From CON
                    deflects=1,  # From INT
                    hit_dice=2,
                    suit_power=6,
                    shield_power=2,
                    death_fails=2,
                    death_successes=3,
                ),
                weapons=CircularList(
                    items=[
                        PilviBR(),
                        PilviGrenadeLauncher(),
                        PilviPistol(),
                        PilviGrenades(),
                        ReplacementSMG(),
                        ]
                ),
            )
        )
