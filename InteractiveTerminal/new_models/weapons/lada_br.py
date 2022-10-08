from .ammo_pack import AmmoPack
from .weapon import Weapon
from ...utils import CircularList, use_passed_or_default
from ..character.stat_block import StatBlock
from ..character.stats import Stat
from ..dice.dice import Dice
from ..dice.advantage import RollStatus
from ..dice.rolls import Roll


class ProjectLadaBR(Weapon):
    def __init__(self, **kwargs):
        super().__init__(
            **use_passed_or_default(
                kwargs,
                name="Project Lada Battle Rifle",
                short_name="Lada BR",
                description=(
                    "A precision made battle rifle for Siren operators, that can "
                    "switch between short bursts and semi-automatic"
                ),
                caliber=6.5,
                range_meters=500,
                clip_current=20,
                clip_capacity=20,
                burst=CircularList(items=[1, 2]),
                mode=CircularList(items=["Standard"]),
                ammo=CircularList(
                    items=[AmmoPack(name="FMJ", current=6 * 12, capacity=6 * 12)]
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
            Dice.D10,
            n_dice=2,
        )
