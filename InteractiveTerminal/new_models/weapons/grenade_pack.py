from .ammo_pack import AmmoPack
from .weapon import Weapon
from ...utils import CircularList, use_passed_or_default
from ..character.stat_block import StatBlock
from ..character.stats import Stat
from ..dice.dice import Dice
from ..dice.advantage import RollStatus
from ..dice.rolls import Roll, CompletedRoll
import typing as T


class GrenadePack(Weapon):
    def __init__(self, **kwargs):
        super().__init__(
            **use_passed_or_default(
                kwargs,
                name="Grenade Pack",
                short_name="Grenade",
                description=("A pack of grenades"),
                range_meters=40,
                clip_current=0,
                clip_capacity=4,
                burst=CircularList(items=[1]),
                mode=CircularList(items=["Thrown"]),
                ammo=CircularList(
                    items=[
                        AmmoPack(
                            name="Flashbang",
                            current=0,
                            capacity=0,
                        ),
                        AmmoPack(
                            name="Concussion",
                            current=0,
                            capacity=0,
                        ),
                        AmmoPack(
                            name="Fragmentation",
                            current=0,
                            capacity=0,
                        ),
                        AmmoPack(
                            name="Smoke",
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
            modifier=equipped_by[Stat.DEXTERITY],
        )

    def _damage_impl(self, equipped_by: StatBlock) -> Roll:
        if self.ammo.get() is not None and self.ammo.get().name == "Concussion":
            return Roll(
                Dice.D6,
                n_dice=6,
            )
        if self.ammo.get() is not None and self.ammo.get(
        ).name == "Fragmentation":
            return Roll(
                Dice.D8,
                n_dice=4,
            )

        return Roll(Dice.D4, 0)

    def get_additional_effects(self, is_attack: bool,
                               roll: CompletedRoll) -> T.Optional[str]:
        if is_attack:
            return None

        if self.ammo.get() is not None and self.ammo.get().name == "Flashbang":
            return (
                "Enemies within 6m make a DC 15 CON save.\nAlways: Blind and deaf, disadvantage on next roll.\nFail: ALSO lose a turn."
            )
        elif self.ammo.get() is not None and self.ammo.get(
        ).name == "Concussion":
            return (
                f"Enemies < 4m take full damage ({roll.total()}). Enemies in < 6m take half damage ({(roll.total() + 1) // 2})"
            )
        elif self.ammo.get() is not None and self.ammo.get(
        ).name == "Fragmentation":
            return (
                f"Enemies < 8m take full damage ({roll.total()}). Enemies in < 12m take half damage ({(roll.total() + 1) // 2})"
            )
        elif self.ammo.get() is not None and self.ammo.get().name == "Smoke":
            return (f"Smoke fills the air.")
        else:
            return None

    def switch_ammo(self) -> bool:
        ret = super().switch_ammo()
        self._set_splash()
        return ret

    def undo_switch_ammo(self, prev_clip: int) -> None:
        super().undo_switch_ammo(prev_clip=prev_clip)
        self._set_splash()

    def _set_splash(self) -> None:
        if self.ammo.get() is not None and self.ammo.get().name == "Flashbang":
            self.splash_meters = 6
        elif self.ammo.get() is not None and self.ammo.get(
        ).name == "Concussion":
            self.splash_meters = 6
        elif self.ammo.get() is not None and self.ammo.get(
        ).name == "Fragmentation":
            self.splash_meters = 12
        elif self.ammo.get() is not None and self.ammo.get().name == "Smoke":
            self.splash_meters = None
