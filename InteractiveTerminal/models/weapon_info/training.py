from ..weapon import Weapon, WeaponAttachment
from ..dice import RollParams
from ..character import Constants


class SpecializedTraining(WeaponAttachment):
    """
    Grants expertise with a weapon
    """
    def attach_to(self, weapon: "Weapon") -> None:
        weapon.add_tag("expert")
    
    def modify_attack(
        self,
        equipped_by: Constants,
        weapon: "Weapon",
        attack: RollParams
    ) -> RollParams:
        return attack.replace(
            modifier=attack.modifier+2*equipped_by.S_PROFICIENCY_BONUS,
        )


class BasicTraining(WeaponAttachment):
    """
    Grants proficiency with a weapon
    """
    def attach_to(self, weapon: "Weapon") -> None:
        weapon.add_tag("proficient")
    
    def modify_attack(
        self,
        equipped_by: Constants,
        weapon: "Weapon",
        attack: RollParams
    ) -> RollParams:
        return attack.replace(
            modifier=attack.modifier+equipped_by.S_PROFICIENCY_BONUS,
        )

