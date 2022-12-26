from .ammo_pack import AmmoPack
from .weapon import Weapon
from ...utils import CircularList, use_passed_or_default
from ..character.stat_block import StatBlock
from ..character.stats import Stat
from ..dice.dice import Dice
from ..dice.advantage import RollStatus
from ..dice.rolls import Roll, CompletedRoll
import typing as T


class SwitchbladeDrone(Weapon):
    def __init__(self, **kwargs):
        super().__init__(
            **use_passed_or_default(
                kwargs,
                name="Reconnaissance/Suicide Drone",
                short_name="Switchblade Drone",
                description=("A light, hand-portable drone with a camera "
                             "and suicide attack capability. Guided weapon."),
                range_meters=100,
                clip_current=0,
                clip_capacity=1,
                mode=CircularList(items=["Thrown"]),
                ammo=CircularList(
                    items=[
                        AmmoPack(
                            name="Drone",
                            current=0,
                            capacity=0,
                        )
                    ]
                ),
            )
        )

    def _attack_impl(self, equipped_by: StatBlock) -> Roll:
        return Roll(
            Dice.D20,
            n_dice=1,
            modifier=equipped_by[Stat.DEXTERITY + Stat.INTELLIGENCE],
        )

    def _damage_impl(self, equipped_by: StatBlock) -> Roll:
        return Roll(Dice.D10, n_dice=7)

    def get_additional_effects(self, is_attack: bool,
                               roll: CompletedRoll) -> T.Optional[str]:
        return (
            f"Enemies < 10m take full damage ({roll.total()}). Enemies in < 20m take half damage ({(roll.total() + 1) // 2})"
        )

    def _set_splash(self) -> None:
        self.splash_meters = 20