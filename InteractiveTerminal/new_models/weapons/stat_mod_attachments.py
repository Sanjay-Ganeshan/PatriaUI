from .weapon import Weapon, WeaponAttachment
from ..dice.rolls import Roll
from ..character.stat_block import StatBlock
from ..character.stats import Stat
import math


class Bipod(WeaponAttachment):
    def attach_to(self, weapon: "Weapon") -> None:
        if weapon.mode.find(lambda m: m == "Braced") is None:
            weapon.mode.append("Braced")
        weapon.add_tag("bipod")

    def modify_attack(
        self, equipped_by: StatBlock, weapon: "Weapon", attack: Roll
    ) -> Roll:
        if weapon.mode.get() == "Braced":
            return attack.replace(
                modifier=attack.modifier +
                ((equipped_by[Stat.PROFICIENCY_BONUS] + 1) // 2),
            )
        else:
            return attack


class VerticalGrip(WeaponAttachment):
    def attach_to(self, weapon: "Weapon") -> None:
        weapon.add_tag("vertical-grip")

    def modify_attack(
        self, equipped_by: StatBlock, weapon: "Weapon", attack: Roll
    ) -> Roll:
        return attack.replace(modifier=attack.modifier + 1, )


class HolographicSight(WeaponAttachment):
    def attach_to(self, weapon: "Weapon") -> None:
        weapon.add_tag("holo-sight")

    def modify_attack(
        self, equipped_by: StatBlock, weapon: "Weapon", attack: Roll
    ) -> Roll:
        return attack.replace(modifier=attack.modifier + 1, )


class TelescopicSight(WeaponAttachment):
    def attach_to(self, weapon: "Weapon") -> None:
        weapon.add_tag("telescopic-sight")

    def modify_attack(
        self, equipped_by: StatBlock, weapon: "Weapon", attack: Roll
    ) -> Roll:
        return attack.replace(
            modifier=attack.modifier +
            ((equipped_by[Stat.PROFICIENCY_BONUS] + 1) // 2),
        )


class Suppressor(WeaponAttachment):
    def attach_to(self, weapon: "Weapon") -> None:
        weapon.add_tag("suppressed")
