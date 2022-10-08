from .ammo_pack import AmmoPack
from .weapon import Weapon
from ...utils import CircularList, use_passed_or_default
from ..character.stat_block import StatBlock
from ..character.stats import Stat
from ..dice.dice import Dice
from ..dice.advantage import RollStatus
from ..dice.rolls import Roll


class ProjectVesnaLSW(Weapon):
    def __init__(self, **kwargs):
        super().__init__(
            **use_passed_or_default(
                kwargs,
                name="Project Vesna - Light Support Weapon",
                short_name="Vesna LSW",
                description=(
                    "A precision made LSW for Siren operators, with a magazine "
                    "feed. Can rapidly fire a hailstorm of bullets. (2x per turn, 3x per turn if using bipod)"
                ),
                caliber=5.3,
                range_meters=400,
                splash_meters=1,
                clip_current=80,
                clip_capacity=80,
                burst=CircularList(items=[10]),
                burst_improves_accuracy=False,
                mode=CircularList(items=["Standard"]),
                ammo=CircularList(
                    items=[
                        AmmoPack(name="FMJ", current=6 * 80, capacity=6 * 80)
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
            Dice.D8,
            n_dice=2,
        )
