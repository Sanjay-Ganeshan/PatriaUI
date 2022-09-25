from ..weapon import Weapon, WeaponAttachment
from ..dice import RollParams
from ..character import Constants
import math


class Bipod(WeaponAttachment):
    def attach_to(self, weapon: "Weapon") -> None:
        weapon.allowed_modes.append("braced")
        weapon.add_tag("bipod")
    
    def modify_attack(
        self, 
        equipped_by: Constants,
        weapon: "Weapon",
        attack: RollParams
    ) -> RollParams:
        if weapon.get_current_mode() == "braced":
            pro = math.ceil(equipped_by.S_PROFICIENCY_BONUS / 2)
            return attack.replace(
                modifier=attack.modifier+pro,
            )
        else:
            return attack
    

class VerticalGrip(WeaponAttachment):
    def attach_to(self, weapon: "Weapon") -> None:
        weapon.add_tag("vertical-grip")
    
    def modify_attack(
        self, 
        equipped_by: Constants,
        weapon: "Weapon",
        attack: RollParams
    ) -> RollParams:
        return attack.replace(
            modifier=attack.modifier+1,
        )
    

class HolographicSight(WeaponAttachment):
    def attach_to(self, weapon: "Weapon") -> None:
        weapon.add_tag("holo-sight")
    
    def modify_attack(
        self, 
        equipped_by: Constants,
        weapon: "Weapon",
        attack: RollParams
    ) -> RollParams:
        return attack.replace(
            modifier=attack.modifier+1,
        )


class TelescopicSight(WeaponAttachment):
    def attach_to(self, weapon: "Weapon") -> None:
        weapon.add_tag("telescopic-sight")
    
    def modify_attack(
        self, 
        equipped_by: Constants,
        weapon: "Weapon",
        attack: RollParams
    ) -> RollParams:
        return attack.replace(
            modifier=attack.modifier+2,
        )


class Suppressor(WeaponAttachment):
    def attach_to(self, weapon: "Weapon") -> None:
        weapon.add_tag("suppressed")

    
class SkinsuitInterface(WeaponAttachment):
    def attach_to(self, weapon: "Weapon") -> None:
        weapon.allowed_modes.append("braced")
        weapon.add_tag("bipod")