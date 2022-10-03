from ...models.character import Constants
from ...models.help_text import HelpText
from .needs_character_mixin import NeedsConstants
from kivy.properties import ObjectProperty



class NeedsWeapon(NeedsConstants):
    bound_weapon: "Weapon" = ObjectProperty(None)

    def weapon_changed(self, *args):
        new_weapon = self.constants.get_active_weapon()
        if self.bound_weapon != new_weapon:
            if self.bound_weapon is not None:
                self.bound_weapon.unbind(self.weapon_modified)
            if new_weapon is not None:
                new_weapon.bind(self.weapon_modified)
            self.bound_weapon = new_weapon

    def weapon_modified(self, wep: "Weapon"):
        pass

    def weapons_init(self):
        self.bind(constants=self.weapon_changed)
