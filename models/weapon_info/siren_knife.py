from ..weapon import Weapon
from dataclasses import dataclass
from ...utils import use_passed_or_default
from ..character import Constants
from ..dice import RollParams, Dice
from ..roll_status import RollStatus

class SirenKnife(Weapon):
    def __init__(self, **kwargs):

        super().__init__(
            **use_passed_or_default(
                kwargs,
                name = "Siren Knife",
                short_name = "Siren Knife",
                description = (
                    "A hardened blade designed for close quarters combat"
                ),
                caliber = 0, # ??
                range_meters = 10,
                loaded_ammo = "Knife",
                ammo_count = {
                    "Knife": (20, 20),
                },
                clip_current = 1,
                clip_capacity = 1,
                allowed_modes = ["Melee", "Thrown"],
                allowed_burst_sizes=[1],
                burst_size_ix=0,
            )
        )

    def fire(self) -> bool:
        """
        Consumes ammo depending on burst size.
        Returns True iff we have enough ammo for the burst
        """
        if self.get_current_mode() == "Melee":
            if self.clip_current > 0:
                return True
            else:
                return False
        else:
            return super().fire()
    
    def _attack_impl(self, equipped_by: Constants) -> RollParams:
        if self.get_current_mode() == "Melee":
            desc = f"{equipped_by.CHARACTER_NAME} stabs with {equipped_by.PRONOUN_HER} knife"
        else:
            desc = f"{equipped_by.CHARACTER_NAME} throws her {equipped_by.PRONOUN_HER} knife (10m)"
        
        return RollParams(
            Dice.D20,
            n_dice=1,
            modifier=equipped_by.S_DEXTERITY,
            description=desc
        )

    def _damage_impl(self, equipped_by: Constants) -> RollParams:
        if self.get_current_mode() == "Melee":
            return RollParams(
                Dice.D10,
                n_dice=3,
                modifier=equipped_by.S_DEXTERITY,
            )
        else:
            return RollParams(
                Dice.D8,
                n_dice=3,
                modifier=equipped_by.S_DEXTERITY,
            )