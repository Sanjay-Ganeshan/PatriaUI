from .ammo_pack import AmmoPack
from .weapon import Weapon
from ...utils import CircularList, use_passed_or_default
from ..character.stat_block import StatBlock
from ..character.stats import Stat
from ..dice.dice import Dice
from ..dice.advantage import RollStatus
from ..dice.rolls import Roll


class RBS(Weapon):
    def __init__(self, **kwargs):
        super().__init__(
            **use_passed_or_default(
                kwargs,
                name="Robotsystem",
                short_name="RBS",
                description="Robotsystem Anti-Air Weapon",
                caliber=127,
                # Idk if this is actually correct
                range_meters=3400,
                clip_current=1,
                clip_capacity=1,
                mode=CircularList(items=["Standard"]),
                ammo=CircularList(
                    items=[AmmoPack(name="Missile", current=2, capacity=2)]
                ),
            )
        )

    def _attack_impl(self, equipped_by: StatBlock) -> Roll:
        return Roll(
            Dice.D20,
            n_dice=1,
            modifier=equipped_by[Stat.DEXTERITY] + equipped_by[Stat.INTELLIGENCE],
        )

    def _damage_impl(self, _equipped_by: StatBlock) -> Roll:
        return Roll(Dice.D12, n_dice=28)
