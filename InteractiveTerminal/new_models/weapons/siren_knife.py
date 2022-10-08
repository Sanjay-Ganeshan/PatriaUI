from .ammo_pack import AmmoPack
from .weapon import Weapon
from ...utils import CircularList, use_passed_or_default
from ..character.stat_block import StatBlock
from ..character.stats import Stat
from ..dice.dice import Dice
from ..dice.advantage import RollStatus
from ..dice.rolls import Roll
import typing as T


class SirenKnife(Weapon):
    def __init__(self, **kwargs):
        super().__init__(
            **use_passed_or_default(
                kwargs,
                name="Siren Knife",
                short_name="Siren Knife",
                description=(
                    "A hardened blade designed for close quarters combat"
                ),
                range_meters=10,
                clip_current=1,
                clip_capacity=1,
                burst=CircularList(items=[1]),
                mode=CircularList(items=["Melee", "Thrown"]),
                ammo=CircularList(
                    items=[
                        AmmoPack(
                            name="Knife",
                            current=1,
                            capacity=1
                        )
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
        if self.mode.get() == "Melee":
            return Roll(
                Dice.D10,
                n_dice=3,
                modifier=equipped_by[Stat.DEXTERITY]
            )
        else:
            return Roll(
                Dice.D8,
                n_dice=3,
                modifier=equipped_by[Stat.DEXTERITY],
            )

    def fire(self) -> bool:
        """
        Consumes ammo depending on burst size.
        Returns True iff we have enough ammo for the burst
        """
        burst_size = self.burst.get() or 0
        if self.mode == "Thrown":
            return super().fire()
        else:
            # Don't consume ammo if melee
            return self.can_fire()

    def load(self, n: T.Optional[int] = None) -> None:
        """
        When you "reload" the knife, you are getting it back
        """
        if self.ammo.get() is not None:
            self.ammo.get().restore(n)
        super().load(n)
        
