from ..weapon import Weapon
from dataclasses import dataclass
from ...utils import use_passed_or_default
from ..character import Constants
from ..dice import RollParams, Dice
from ..roll_status import RollStatus

class CoalitionPistol(Weapon):
    def __init__(self, **kwargs):

        super().__init__(
            **use_passed_or_default(
                kwargs,
                name = "Coalition Pistol",
                short_name = "Pistol",
                description = (
                    "A standard issue pistol"
                ),
                caliber = 9,
                range_meters = 40,
                loaded_ammo = "FMJ",
                ammo_count = {
                    "FMJ": (4*12, 4*12),
                },
                clip_current = 12,
                clip_capacity = 12,
                allowed_modes = ["Standard"],
                allowed_burst_sizes=[1],
            )
        )
    
    def _attack_impl(self, equipped_by: Constants) -> RollParams:
        return RollParams(
            Dice.D20,
            n_dice=1,
            modifier=equipped_by.S_DEXTERITY,
        )

    def _damage_impl(self, equipped_by: Constants) -> RollParams:
        return RollParams(
            Dice.D4,
            n_dice=2,
        )