from ..weapon import Weapon
from dataclasses import dataclass
from ...utils import use_passed_or_default
from ..character import Constants
from ..dice import RollParams, Dice
from ..roll_status import RollStatus

class ProjectVesnaLSW(Weapon):
    def __init__(self, **kwargs):

        super().__init__(
            **use_passed_or_default(
                kwargs,
                name = "Project Vesna - Light Support Weapon",
                short_name = "Vesna LSW",
                description = (
                    "A precision made LSW for Siren operators, with a magazine "
                    "feed. Can rapidly fire a hailstorm of bullets. (2x per turn, 3x per turn if using bipod)"
                ),
                caliber = 5.3, # ??
                range_meters = 400,
                loaded_ammo = "FMJ",
                ammo_count = {
                    "FMJ": (6*80, 6*80),
                },
                clip_current = 80,
                clip_capacity = 80,
                allowed_modes = ["Standard"],
                allowed_burst_sizes=[10], # Does not get bonus
                burst_improves_accuracy = False,
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
            Dice.D8,
            n_dice=2,
        )