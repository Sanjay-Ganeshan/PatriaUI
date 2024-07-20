from .ammo_pack import AmmoPack
from .weapon import Weapon
from ...utils import CircularList, use_passed_or_default
from ..character.stat_block import StatBlock
from ..character.stats import Stat
from ..dice.dice import Dice
from ..dice.rolls import Roll


class ProjectLadaAR(Weapon):
    def __init__(self, **kwargs):
        super().__init__(
            **use_passed_or_default(
                kwargs,
                name="Project Lada Assult Rifle",
                short_name="Lada BR",
                description=(
                    "A precision made assult rifle for Siren operators, that can "
                    "switch between short bursts, semi-automatic and fully automatic"
                ),
                caliber=6.5,
                range_meters=300,
                clip_current=28,
                clip_capacity=28,
                burst=CircularList(items=[1, 4]),
                mode=CircularList(items=["Standard"]),
                ammo=CircularList(
                    items=[AmmoPack(name="FMJ", current=8 * 28, capacity=8 * 28)]
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
            Dice.D8,
            n_dice=2,
        )
