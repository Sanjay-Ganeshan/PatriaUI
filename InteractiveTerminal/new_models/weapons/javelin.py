from .ammo_pack import AmmoPack
from .weapon import Weapon
from ...utils import CircularList, use_passed_or_default
from ..character.stat_block import StatBlock
from ..character.stats import Stat
from ..dice.dice import Dice
from ..dice.advantage import RollStatus
from ..dice.rolls import Roll


class Javelin(Weapon):
    def __init__(self, **kwargs):
        super().__init__(
            **use_passed_or_default(
                kwargs,
                name="Javelin",
                short_name="Javelin",
                description="Javelin Anti-Tank Weapon",
                caliber=127,
                # Idk if this is actually correct
                range_meters=400,
                clip_current=1,
                clip_capacity=1,
                mode=CircularList(items=["Standard"]),
                ammo=CircularList(
                    items=[AmmoPack(name="Javelin", current=2, capacity=2)]
                ),
            )
        )

    def _attack_impl(self, equipped_by: StatBlock) -> Roll:
        return Roll(
            Dice.D20,
            n_dice=1,
            modifier=equipped_by[Stat.DEXTERITY],
        )

    def _damage_impl(self, _equipped_by: StatBlock) -> Roll:
        return Roll(Dice.D12, n_dice=28)
