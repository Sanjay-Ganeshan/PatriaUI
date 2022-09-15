from ..weapon import Weapon
from dataclasses import dataclass
from ...utils import use_passed_or_default
from ..character import Constants
from ..dice import RollParams, Dice
from ..roll_status import RollStatus

class ProjectSplazer(Weapon):
    def __init__(self, **kwargs):

        super().__init__(
            **use_passed_or_default(
                kwargs,
                name = "Splazer",
                short_name = "Splazer",
                description = (
                    "Affectionately called the Splazer, this top-secret, cutting edge laser "
                    "weapon deals massive damage. A select number of Sirens have "
                    "been equipped with it to test its efficacy. "
                    "Please remember to properly file a "
                    "usage report with HQ if you use ammunition from this weapon."
                ),
                caliber = 117,
                range_meters = 100,
                loaded_ammo = "Laser",
                ammo_count = {
                    "Laser": (1, 1),
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
            modifier=equipped_by.S_DEXTERITY,
        )

    def _damage_impl(self, equipped_by: Constants) -> RollParams:
        return RollParams(
            Dice.D20,
            n_dice=1000,
        )