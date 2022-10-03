from ..weapon import Weapon
from dataclasses import dataclass
from ...utils import use_passed_or_default
from ..character import Constants
from ..dice import RollParams, Dice
from ..roll_status import RollStatus
import math

class UnderbarrelGrenadeLauncher(Weapon):
    def __init__(self, **kwargs):
        super().__init__(
            **use_passed_or_default(
                kwargs,
                name = "Underbarrel Grenade Launcher",
                short_name = "Grenade Launcher",
                description = (
                    "A grenade launcher attached to your primary weapon. "
                    "Deals damage in an 8 meter radius. On a DEX save "
                    "of 15 or higher, damage is mitigated by half"
                ),
                caliber = 40,
                range_meters = 400,
                loaded_ammo = "Grenade",
                ammo_count = {
                    "Grenade": (4, 4),
                },
                clip_current = 1,
                clip_capacity = 1,
                allowed_modes = ["Standard"],
                allowed_burst_sizes=[1],
            )
        )
    
    def _attack_impl(self, equipped_by: Constants) -> RollParams:
        return RollParams(
            Dice.D20,
            n_dice=1,
        )

    def _damage_impl(self, equipped_by: Constants) -> RollParams:
        return RollParams(
            Dice.D6,
            n_dice=4,
            post_roll_desc=lambda total, raw:f"8m splash damage, reduced to {(total+1) // 2} on a successful dex save of 15",
        )