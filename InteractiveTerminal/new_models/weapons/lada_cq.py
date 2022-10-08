from .ammo_pack import AmmoPack
from .weapon import Weapon
from ...utils import CircularList, use_passed_or_default
from ..character.stat_block import StatBlock
from ..character.stats import Stat
from ..dice.dice import Dice
from ..dice.advantage import RollStatus
from ..dice.rolls import Roll


class ProjectLadaCQ(Weapon):
    def __init__(self, **kwargs):
        super().__init__(
            **use_passed_or_default(
                kwargs,
                name="Project Lada Close-Quarters",
                short_name="Lada CQ",
                description=(
                    "An SMG specially designed for Sirens. Can attack twice per turn."
                ),
                caliber=9,
                range_meters=120,
                clip_current=40,
                clip_capacity=40,
                burst=CircularList(items=[1, 8]),
                mode=CircularList(items=["Standard"]),
                ammo=CircularList(
                    items=[
                        AmmoPack(
                            name="FMJ",
                            current=4 * 40,
                            capacity=4 * 40
                        )
                    ]
                ),
            )
        )

    def _attack_impl(self, equipped_by: StatBlock) -> Roll:
        return Roll(
            Dice.D20,
            n_dice=1,
            modifier=equipped_by[Stat.DEXTERITY],
        )

    def _damage_impl(self, equipped_by: StatBlock) -> Roll:
        return Roll(
            Dice.D6,
            n_dice=2,
        )
