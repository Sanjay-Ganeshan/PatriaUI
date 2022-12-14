from .ammo_pack import AmmoPack
from .weapon import Weapon
from ...utils import CircularList, use_passed_or_default
from ..character.stat_block import StatBlock
from ..character.stats import Stat
from ..dice.dice import Dice
from ..dice.advantage import RollStatus
from ..dice.rolls import Roll


class CoalitionPistol(Weapon):
    def __init__(self, **kwargs):
        super().__init__(
            **use_passed_or_default(
                kwargs,
                name="Coalition Pistol",
                short_name="Pistol",
                description=("A standard issue pistol"),
                caliber=9,
                range_meters=40,
                clip_current=12,
                clip_capacity=12,
                burst=CircularList(items=[1]),
                mode=CircularList(items=["Standard"]),
                ammo=CircularList(
                    items=[
                        AmmoPack(
                            name="Parabellum", current=4 * 12, capacity=4 * 12
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
            Dice.D4,
            n_dice=2,
        )
