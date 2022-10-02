from ..weapon import Weapon
from dataclasses import dataclass
from ...utils import use_passed_or_default
from ..character import Constants
from ..dice import RollParams, Dice
from ..roll_status import RollStatus

class ProjectLadaSMG(Weapon):
    def __init__(self, **kwargs):
        super().__init__(
            **use_passed_or_default(
                kwargs,
                name = "Project Lada Close-Quarters",
                short_name = "Lada CQ",
                description = (
                    "An SMG specially designed for Sirens"
                ),
                caliber = 9,
                range_meters = 120,
                loaded_ammo = "FMJ",
                ammo_count = {
                    "FMJ": (4*40, 4*40),
                },
                clip_current = 40,
                clip_capacity = 40,
                allowed_modes = ["Standard"],
                allowed_burst_sizes=[1, 8],
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
            Dice.D6,
            n_dice=2,
        )