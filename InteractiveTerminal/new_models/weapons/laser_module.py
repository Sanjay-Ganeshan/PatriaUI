from .ammo_pack import AmmoPack
from .weapon import Weapon
from ...utils import CircularList, use_passed_or_default
from ..character.stat_block import StatBlock
from ..character.stats import Stat
from ..dice.dice import Dice
from ..dice.advantage import RollStatus
from ..dice.rolls import Roll


class UnderbarrelLaser(Weapon):
    def __init__(self, **kwargs):
        super().__init__(
            **use_passed_or_default(
                kwargs,
                name="Laser Module attachment",
                short_name="Laser",
                description=(
                    "Laser Module Attachment. Bonus Action - blind an enemy in 10m. Con Save, DC 15, grants disadvantage on attack rolls / skill checks."
                ),
                caliber=0,
                range_meters=10,
                clip_current=100,
                clip_capacity=100,
                burst=CircularList(items=[1]),
                mode=CircularList(items=["Blind"]),
                ammo=CircularList(
                    items=[
                        AmmoPack(name="Laser", current=100, capacity=100)
                    ]
                ),
            )
        )

    def _attack_impl(self, equipped_by: StatBlock) -> Roll:
        return Roll(
            Dice.D20,
            n_dice=0,
            modifier=equipped_by[Stat.DEXTERITY],
        )

    def _damage_impl(self, equipped_by: StatBlock) -> Roll:
        return Roll(
            Dice.D6,
            n_dice=0,
        )
