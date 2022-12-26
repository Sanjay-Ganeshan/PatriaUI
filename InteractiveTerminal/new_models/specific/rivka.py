from ...utils import use_passed_or_default, CircularList
from ..character.active_effects import Debuffs
from ..character.character import Character
from ..character.nameplate import Nameplate
from ..character.proficiencies import Proficiency
from ..character.stat_block import StatBlock
from ..character.stats import Stat
from ..character.status import Status

# change this
from ..weapons.character_specific_weapons import (
    RivkaSniper, RivkaPistol, RivkaGrenades, ReplacementSMG,
)


class RivkaHadar(Character):
    def __init__(self, **kwargs) -> None:
        super().__init__(
            **use_passed_or_default(
                kwargs,
                id_prefix="rivka",
                nameplate=Nameplate(
                    icon="gfl_sv98.png",
                    name="Rivka",
                    surname="Hadar",
                    role="Siren - Sniper",
                    she="she",
                    her="her",
                    hers="hers",
                ),
                stat_block=StatBlock.create(
                    assignments=[
                        (Stat.STRENGTH, -1),
                        (Stat.DEXTERITY, 2),
                        (Stat.CONSTITUTION, 0),
                        (Stat.INTELLIGENCE, 2),
                        (Stat.WISDOM, 1),
                        (Stat.PROFICIENCY_BONUS, 4),
                        (Proficiency.ATHLETICS, 1),
                        (Proficiency.COMBATIVES, 1),
                        (Proficiency.STEALTH, 1),
                        (Proficiency.INVESTIGATION, 1),
                        (Proficiency.INSIGHT, 1),
                        (Proficiency.MEDICINE, 1),
                        (Proficiency.PERCEPTION, 1),
                    ],
                ),
                current_life=None,
                max_life=Status(
                    HP=12,
                    armor_rating=14,
                    revives=1,  # From CON
                    deflects=2,  # From INT
                    hit_dice=2,
                    suit_power=6,
                    shield_power=2,
                    death_fails=2,
                    death_successes=3,
                ),

                # modify this
                weapons=CircularList(
                    items=[
                        RivkaSniper(),
                        RivkaPistol(),
                        RivkaGrenades(),
                        ReplacementSMG(),
                    ],
                ),
            )
        )
