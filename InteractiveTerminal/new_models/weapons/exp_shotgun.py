from .ammo_pack import AmmoPack
from .weapon import Weapon
from ...utils import CircularList, use_passed_or_default
from ..character.stat_block import StatBlock
from ..character.stats import Stat
from ..dice.dice import Dice
from ..dice.advantage import RollStatus
from ..dice.rolls import Roll


class ExperimentalShotgun(Weapon):
    def __init__(self, **kwargs):
        super().__init__(
            **use_passed_or_default(
                kwargs,
                name="Project Lada/Vesna Tactical Shotgun",
                short_name="Experimental SG",
                description=(
                    "Experimental Project Lada/Vesna compatiable shotgun. "
                    "Fabricated on-site by Transcendent's engineering teams; "
                    "capable of 2-round ultra-rapid bursts. Advantage on attack "
                    "rolls within 20 meters."
                ),
                caliber=18,
                range_meters=40,
                clip_current=8,
                clip_capacity=8,
                burst=CircularList(items=[1, 2]),
                mode=CircularList(items=["Standard"]),
                ammo=CircularList(
                    items=[
                        AmmoPack(name="FMJ", current=5 * 8, capacity=5 * 8),
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
            n_dice=4,
        )
