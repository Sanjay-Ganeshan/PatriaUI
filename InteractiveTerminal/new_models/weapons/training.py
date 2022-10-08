from .weapon import Weapon, WeaponAttachment
from ..dice.rolls import Roll
from ..character.stat_block import StatBlock
from ..character.stats import Stat


class SpecializedTraining(WeaponAttachment):
    """
    Grants expertise with a weapon
    """
    def attach_to(self, weapon: "Weapon") -> None:
        weapon.add_tag("expert")

    def modify_attack(
        self, equipped_by: StatBlock, weapon: "Weapon", attack: Roll
    ) -> Roll:
        return attack.replace(
            modifier=attack.modifier + 2 * equipped_by[Stat.PROFICIENCY_BONUS],
        )


class BasicTraining(WeaponAttachment):
    """
    Grants proficiency with a weapon
    """
    def attach_to(self, weapon: "Weapon") -> None:
        weapon.add_tag("proficient")

    def modify_attack(
        self, equipped_by: StatBlock, weapon: "Weapon", attack: Roll
    ) -> Roll:
        return attack.replace(
            modifier=attack.modifier + equipped_by[Stat.PROFICIENCY_BONUS],
        )
