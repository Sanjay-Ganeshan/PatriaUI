from .ammo_pack import AmmoPack
from .weapon import Weapon
from ...utils import CircularList, use_passed_or_default
from ..character.stat_block import StatBlock
from ..character.stats import Stat
from ..dice.dice import Dice
from ..dice.advantage import RollStatus
from ..dice.rolls import Roll


class ProjectLadaSniper(Weapon):
    def __init__(self, **kwargs):
        super().__init__(
            **use_passed_or_default(
                kwargs,
                name="Project Lada Sniper Rifle",
                short_name="Lada SR",
                description=(
                    "Conversion kit for the Project Lada platform; turns "
                    "the gun into a bolt-action sniper rifle for long-range "
                    "precision fire. As a bolt-action rifle, cannot jam. "
                    "Conversion kit incompatible with the Project Vesna prototypes."
                ),
                caliber=7.8,
                range_meters=1750,
                clip_current=0,
                clip_capacity=4,
                mode=CircularList(items=["Standard"]),
                ammo=CircularList(
                    items=[
                        AmmoPack(name="FMJ", current=6 * 4, capacity=6 * 4)
                    ]
                ),
            )
        )

    def _attack_impl(self, equipped_by: StatBlock) -> Roll:
        return Roll(
            Dice.D20,
            n_dice=1,
            modifier=equipped_by[Stat.DEXTERITY] + 1,
        )

    def _damage_impl(self, equipped_by: StatBlock) -> Roll:
        return Roll(
            Dice.D12,
            n_dice=2,
        )
