from .ammo_pack import AmmoPack
from .weapon import Weapon, WeaponAttachment
from ..dice.rolls import Roll
from ..character.stat_block import StatBlock
from ..character.stats import Stat


class PlasmaChamber(WeaponAttachment):
    """
    Allows a weapon to fire plasma rounds
    """
    def attach_to(self, weapon: "Weapon") -> None:
        if weapon.ammo.find(lambda pack: pack.name == "Plasma") is None:
            weapon.ammo.append(
                AmmoPack(
                    name="Plasma",
                    current=0,
                    capacity=0,
                )
            )
            weapon.replace_magazine("FMJ", "Plasma")

    def modify_damage(
        self, equipped_by: StatBlock, weapon: "Weapon", damage: Roll
    ) -> Roll:
        ammo = weapon.ammo.get()
        if ammo is not None and ammo.name == "Plasma":
            return damage.replace(n_dice=damage.n_dice + 1, )
        else:
            return damage


class EMChamber(WeaponAttachment):
    """
    Allows a weapon to fire EM rounds
    """
    def attach_to(self, weapon: "Weapon") -> None:
        if weapon.ammo.find(lambda pack: pack.name == "EM") is None:
            weapon.ammo.append(AmmoPack(
                name="EM",
                current=0,
                capacity=0,
            ))
            weapon.replace_magazine("FMJ", "EM")


class APChamber(WeaponAttachment):
    """
    Allows a weapon to fire armor piercing rounds
    """
    def attach_to(self, weapon: "Weapon") -> None:
        if weapon.ammo.find(lambda pack: pack.name == "AP") is None:
            weapon.ammo.append(AmmoPack(
                name="AP",
                current=0,
                capacity=0,
            ))
            weapon.replace_magazine("FMJ", "AP")

    def modify_attack(
        self, equipped_by: StatBlock, weapon: "Weapon", attack: Roll
    ) -> Roll:
        ammo = weapon.ammo.get()
        if ammo is not None and ammo.name == "AP":
            return attack.replace(modifier=attack.modifier + 1, )
        else:
            return attack
