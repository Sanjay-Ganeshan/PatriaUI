from ..weapon import Weapon
from dataclasses import dataclass
from ...utils import use_passed_or_default
from ..character import Constants
from ..dice import RollParams, Dice
from ..roll_status import RollStatus

class ProjectLadaBR(Weapon):
    def __init__(self, **kwargs):

        super().__init__(
            **use_passed_or_default(
                kwargs,
                name = "Project Lada Battle Rifle",
                short_name = "Lada BR",
                description = (
                    "A precision made battle rifle for Siren operators, that can "
                    "switch between short bursts and semi-automatic"
                ),
                caliber = 7.8, # ??
                range_meters = 500,
                loaded_ammo = "FMJ",
                ammo_count = {
                    "FMJ": (6*20, 6*20),
                },
                clip_current = 20,
                clip_capacity = 20,
                allowed_modes = ["Standard"],
                allowed_burst_sizes=[1, 2],
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
            Dice.D10,
            n_dice=2,
        )