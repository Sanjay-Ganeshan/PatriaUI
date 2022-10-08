from .ammo_pack import AmmoPack
from .weapon import Weapon
from ...utils import CircularList, use_passed_or_default
from ..character.stat_block import StatBlock
from ..character.stats import Stat
from ..dice.dice import Dice
from ..dice.advantage import RollStatus
from ..dice.rolls import Roll, CompletedRoll
import typing as T


class UnderbarrelGrenadeLauncher(Weapon):
    def __init__(self, **kwargs):
        super().__init__(
            **use_passed_or_default(
                kwargs,
                name="Underbarrel Grenade Launcher",
                short_name="Grenade Launcher",
                description=(
                    "A grenade launcher attached to your primary weapon. "
                    "Deals damage in an 8 meter radius. On a DEX save "
                    "of 15 or higher, damage is mitigated by half"
                ),
                caliber=40,
                range_meters=400,
                splash_meters=8,
                clip_current=1,
                clip_capacity=1,
                burst=CircularList(items=[1]),
                mode=CircularList(items=["Underbarrel"]),
                ammo=CircularList(
                    items=[AmmoPack(
                        name="Grenade",
                        current=4,
                        capacity=4,
                    )]
                ),
            )
        )

    def _attack_impl(self, equipped_by: StatBlock) -> Roll:
        return Roll(
            Dice.D20,
            n_dice=1,
        )

    def _damage_impl(self, equipped_by: StatBlock) -> Roll:
        return Roll(
            Dice.D6,
            n_dice=4,
        )

    def get_additional_effects(self, is_attack: bool,
                               roll: CompletedRoll) -> T.Optional[str]:
        if not is_attack:
            return f"Targets must make a DEX save (DC 15). Success - half damage ({(roll.total()+1) // 2})"
        else:
            return None
