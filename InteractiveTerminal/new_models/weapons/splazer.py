from .ammo_pack import AmmoPack
from .weapon import Weapon
from ...utils import CircularList, use_passed_or_default
from ..character.stat_block import StatBlock
from ..character.stats import Stat
from ..dice.dice import Dice
from ..dice.advantage import RollStatus
from ..dice.rolls import Roll


class Splazer(Weapon):
    def __init__(self, **kwargs):
        super().__init__(
            **use_passed_or_default(
                kwargs,
                name="XM786 Experimental Directed Energy Weapon",
                short_name="XM786",
                description=(
                    "Affectionately called the Splazer, this top-secret, cutting edge laser "
                    "weapon deals massive damage to EVERYTHING in a 100m straight line.\n"
                    "A select number of Sirens have "
                    "been equipped with it to test its efficacy.\n"
                    "Please remember to file a "
                    "usage report with HQ if you use ammunition from this weapon."
                ),
                range_meters=100,
                splash_meters=0.01,
                clip_current=1,
                clip_capacity=1,
                burst=CircularList(items=[1]),
                mode=CircularList(items=["Beam"]),
                ammo=CircularList(
                    items=[AmmoPack(name="Laser", current=1, capacity=1)]
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
            Dice.D20,
            n_dice=1000,
        )
