from ..weapon import Weapon, WeaponAttachment
from ..dice import RollParams
from ..character import Constants

class PlasmaChamber(WeaponAttachment):
    """
    Allows a weapon to fire plasma rounds
    """
    def attach_to(self, weapon: "Weapon") -> None:
        if "Plasma" not in weapon.ammo_count:
            weapon.ammo_count["Plasma"] = (0, 0)
            weapon.replace_magazine("FMJ", "Plasma")
    
    
    def modify_damage(
        self, 
        equipped_by: Constants,
        weapon: "Weapon",
        damage: RollParams
    ) -> RollParams:
        if weapon.loaded_ammo == "Plasma":
            return damage.replace(
                n_dice=damage.n_dice+1,
            )
        else:
            return damage



class EMChamber(WeaponAttachment):
    """
    Allows a weapon to fire EM rounds
    """
    def attach_to(self, weapon: "Weapon") -> None:
        if "EM" not in weapon.ammo_count:
            weapon.ammo_count["EM"] = (0,0)
            weapon.replace_magazine("FMJ", "EM")

    def modify_damage(
        self, 
        equipped_by: Constants,
        weapon: "Weapon",
        damage: RollParams
    ) -> RollParams:
        if weapon.loaded_ammo == "EM":
            return damage.replace(
                post_roll_desc=lambda tot,r:"This damage ignores shields."
            )
        else:
            return damage

class APChamber(WeaponAttachment):
    """
    Allows a weapon to fire armor piercing rounds
    """
    def attach_to(self, weapon: "Weapon") -> None:
        if "AP" not in weapon.ammo_count:
            weapon.ammo_count["AP"] = (0, 0)
            weapon.replace_magazine("FMJ", "AP")
    
    def modify_attack(self, equipped_by: Constants, weapon: "Weapon", attack: RollParams) -> RollParams:
        if weapon.loaded_ammo == "AP":
            return attack.replace(
                modifier=attack.modifier+1,
            )
        else:
            return attack
    
        
