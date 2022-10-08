from .ammo_pack import AmmoPack
from .weapon import Weapon
from ...utils import CircularList, use_passed_or_default
from ..character.stat_block import StatBlock
from ..character.stats import Stat
from ..dice.dice import Dice
from ..dice.advantage import RollStatus
from ..dice.rolls import Roll


class ProjectLadaDMR(Weapon):
    def __init__(self, **kwargs):
        super().__init__(
            **use_passed_or_default(
                kwargs,
                name="Project Lada Designated Marksman's Rifle",
                short_name="Lada DMR",
                description=(
                    "A precision made rifle for Siren operators that can fire a "
                    "full power cartridge and take down a target from a great distance."
                ),
                caliber=7.8,
                range_meters=1200,
                clip_current=0,
                clip_capacity=12,
                mode=CircularList(items=["Standard"]),
                ammo=CircularList(
                    items=[
                        AmmoPack(name="FMJ", current=8 * 12, capacity=8 * 12)
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
            Dice.D12,
            n_dice=2,
        )
