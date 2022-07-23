from ..weapon import Weapon
from dataclasses import dataclass
from ...utils import use_passed_or_default
from ..character import Constants
from ..dice import RollParams, Dice
from ..roll_status import RollStatus

class ProjectLadaDMR(Weapon):
    def __init__(self, **kwargs):

        super().__init__(
            **use_passed_or_default(
                kwargs,
                name = "Project Lada Designated Marksman's Rifle",
                short_name = "Lada DMR",
                description = (
                    "A precision made rifle for Siren operators that can fire a "
                    "full power cartridge and take down a target from a great distance."
                ),
                caliber = 7.8,
                range_meters = 1200,
                loaded_ammo = "FMJ",
                ammo_count = {
                    "FMJ": 60,
                },
                clip_current = 0,
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
            Dice.D12,
            n_dice=2,
        )