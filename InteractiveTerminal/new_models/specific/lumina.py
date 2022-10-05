from ..character.nameplate import Nameplate
from ..character.character import Character
from ..character.stat_block import StatBlock
from ..character.stats import Stat
from ..character.status import Status
from ..character.proficiencies import Proficiency

import typing as T
from dataclasses import dataclass

from ...utils import use_passed_or_default


class LuminaGale(Character):
    def __init__(self, **kwargs) -> None:
        super().__init__(
            **use_passed_or_default(
                kwargs,
                id_prefix="lumina",
                nameplate=Nameplate(
                    icon="sinon3.png",
                    name="Lumina Gale",
                    role="Siren - Sniper",
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
                        (Proficiency.ATHLETICS, 1),
                        (Proficiency.COMBATIVES, 1),
                        (Proficiency.ACROBATICS, 2),
                        (Proficiency.STEALTH, 2),
                        (Proficiency.INVESTIGATION, 1),
                        (Proficiency.MEDICINE, 1),
                        (Proficiency.PERCEPTION, 1),
                    ],
                    proficiency_bonus=4,
                ),
                current_life=None,
                max_life=Status(
                    HP=13,
                    armor_rating=14,
                    revives=2,  # From CON
                    deflects=2,  # From INT
                    hit_dice=2,
                    suit_power=6,
                    shield_power=2,
                    death_fails=2,
                    death_successes=3,
                ),
                active_effects=[],
            )
        )