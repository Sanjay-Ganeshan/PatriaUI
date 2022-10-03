from ..weapon import Weapon
from dataclasses import dataclass
from ...utils import use_passed_or_default
from ..character import Constants
from ..dice import RollParams, Dice
from ..roll_status import RollStatus

class GrenadePack(Weapon):
    def __init__(self, **kwargs):

        super().__init__(
            **use_passed_or_default(
                kwargs,
                name = "Grenade Pack",
                short_name = "Grenades",
                description = (
                    "A pack of grenades"
                ),
                caliber = 9,
                range_meters = 40,
                loaded_ammo = "Flashbang",
                ammo_count = {
                    "Flashbang": (0, 4),
                    "Concussion": (0, 4),
                    "Fragmentation": (0, 4),
                    "Smoke": (0, 4),
                },
                clip_current = 4,
                clip_capacity = 4,
                allowed_modes = ["Thrown"],
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
        if self.loaded_ammo == "Flashbang":
            return RollParams(
                Dice.D8,
                description=f"{equipped_by.CHARACTER_NAME}'s flashbang grenade explodes. 6m AoE CON save (DC 15). Pass - disadvantage, blind and deaf. Fail - Also lose your turn.",
                n_dice=0,
            )
        if self.loaded_ammo == "Concussion":
            return RollParams(
                Dice.D6,
                n_dice=6,
                description=f"{equipped_by.CHARACTER_NAME}'s concussion grenade explodes",
                post_roll_desc=lambda total,raw: f"{total} lethal damage (4m), {(total+1) // 2} wounding damage (6m)"
            )
        if self.loaded_ammo == "Smoke":
            return RollParams(
                Dice.D8,
                description=f"{equipped_by.CHARACTER_NAME}'s smoke grenade explodes. Smoke fills the air. No damage.",
                n_dice=0,
            )
        if self.loaded_ammo == "Fragmentation":
            return RollParams(
                Dice.D8,
                n_dice=4,
                description=f"{equipped_by.CHARACTER_NAME}'s frag grenade explodes",
                post_roll_desc=lambda total,raw: f"{total} lethal damage (8m), {(total+1) // 2} wounding damage (12m)"
            )
        else: 
            return RollParams(
                Dice.D2,
                description="UNKNOWN",
            )