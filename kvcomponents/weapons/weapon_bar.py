from sympy import maximum
from ...models.weapon import Weapon
from ...models.character import Constants
from ..shared.centered_label import CenteredLabel
from ..shared.tooltip import OptionalTooltip
from ..shared.progressive_icon import ProgressiveText
from kivymd.uix.boxlayout import MDBoxLayout
from ..shared.box_sized_mixin import BoxSized
from ..shared.needs_character_mixin import NeedsConstants
from ..shared.needs_weapon_mixin import NeedsWeapon
from ...models.game import THE_GAME
from ...models.app_settings import BOX_HEIGHT, BOX_WIDTH
from kivy.uix.image import Image
from ..resource_list import Resources
from ..shared.touchable_mixin import TouchableMixin
from ..shared.spacer import Spacer



class WPAmmoSwitcher:
    """
    Swap ammo
    """
    pass


class WPModeSwitcher:
    """
    Swap modes
    """
    pass


class WPAmmoCount(ProgressiveText, NeedsWeapon, TouchableMixin):
    """
    Reload + consume ammo
    """
    def __init__(self, **kwargs):
        super().__init__(
            source=Resources.BULLET_LEFT,
            box_width=1.5,
            box_height=2,
            current_value=1,
            maximum_value=1,
            pr_empty_color="black",
            pr_full_color="gold",
            halign="center",
            valign="bottom",
            font_style="H6",
            **kwargs,
        )
        self.constants_init()
        self.weapons_init()
        self.touch_init()


    def weapon_changed(self, *args):
        super().weapon_changed(*args)
        if self.bound_weapon is not None:
            self.current_value = self.bound_weapon.clip_current
            self.maximum_value = self.bound_weapon.clip_capacity

    def weapon_modified(self, wep):
        super().weapon_modified(wep)
        if self.bound_weapon is not None:
            self.current_value = self.bound_weapon.clip_current
            self.maximum_value = self.bound_weapon.clip_capacity

    def on_left_click(self, position):
        super().on_left_click(position)
        if self.bound_weapon is not None:
            self.bound_weapon.fire()
    
    def on_right_click(self, position):
        super().on_right_click(position)
        if self.bound_weapon is not None:
            self.bound_weapon.reload()

    def get_text(self):
        if self.bound_weapon is not None:
            cur = self.bound_weapon.clip_current
            mx = self.bound_weapon.clip_capacity
            ammo_max = self.bound_weapon._get_current_ammo()
            return f"{cur} / {mx} ({ammo_max - cur})"
        else:
            return "?"
        

class WPBurstSize(CenteredLabel, NeedsWeapon, TouchableMixin):
    """
    Toggle burst size
    """
    def __init__(self, **kwargs):
        super().__init__(
            text="3x",
            font_style="H4",
            **kwargs,
        )
        self.constants_init()
        self.touch_init()
        self.weapons_init()

    def weapon_changed(self, *args):
        super().weapon_changed(*args)
        if self.bound_weapon is not None:
            pass

    def weapon_modified(self, wep: "Weapon"):
        super().weapon_modified(wep)
        if self.bound_weapon is not None:
            pass

class WPIcon(Image, BoxSized, NeedsConstants, TouchableMixin, OptionalTooltip):
    def __init__(self, **kwargs):
        super().__init__(
            source="",
            box_width=3,
            box_height=2,
            allow_stretch=True,
            **kwargs,
        )
        self.box_init()
        self.constants_init()
        self.touch_init()

    def adapt_to_constants(self, *args):
        super().adapt_to_constants(*args)
        wep = self.constants.get_active_weapon()
        self.source = Resources.WEAPON_ICONS.get(
            wep.short_name,
            Resources.DEATH_FAIL,
        )
        self.tooltip_text = f"{wep.name}\n{wep.description}"
    
    def on_left_click(self, position):
        super().on_left_click(position)
        THE_GAME.adjust_current_character(
            ACTIVE_WEAPON=((self.constants.ACTIVE_WEAPON + 1) % len(self.constants.WEAPONS))
        )

class WPWeaponName(CenteredLabel, NeedsConstants, TouchableMixin):
    def __init__(self, **kwargs):
        super().__init__(
            text="ttt",
            box_width=2,
            box_height=2,
            **kwargs,
        )
        self.constants_init()
        
    
    def adapt_to_constants(self, *args):
        super().adapt_to_constants(*args)
        wep = self.constants.get_active_weapon()
        self.text = wep.short_name  

class WPAttackOrDamageIcon(BoxSized, Image, TouchableMixin, NeedsWeapon):
    def __init__(self, which_func, **kwargs):
        self.which_func = which_func
        super().__init__(
            source=Resources.BLOOD if self.which_func == "damage" else Resources.RETICLE,
            box_width=0.5,
            box_height=2,
            color="darkred",
            **kwargs
        )
        self.constants_init()
        self.weapons_init()
        self.touch_init()
    
    def on_left_click(self, position):
        super().on_left_click(position)
        if self.bound_weapon is not None and self.constants is not None:
            getattr(self.bound_weapon, self.which_func)(self.constants).roll()
    
class WPAttackOrDamage(MDBoxLayout, BoxSized, NeedsWeapon):
    def __init__(self, which_func, **kwargs):
        assert which_func in ["damage", "attack"], f"bad {which_func}"
        self.which_func = which_func
        super().__init__(
            **kwargs,
            orientation="horizontal",
            box_width=2.5,
            box_height=2,
        )
        self.box_init()
        self.constants_init()
        self.weapons_init()
        
        self.icon = WPAttackOrDamageIcon(which_func)
        self.dmg = CenteredLabel(box_width=2, box_height=2, halign="left", font_style="H5")
        self.add_widget(self.icon)
        self.add_widget(self.dmg)

    def weapon_modified(self, wep: "Weapon"):
        super().weapon_modified(wep)
        if self.bound_weapon is not None:
            self.dmg.text = str(getattr(self.bound_weapon, self.which_func)(self.constants))

    
    def weapon_changed(self, *args):
        super().weapon_changed(*args)

        if self.bound_weapon is not None:
            self.dmg.text = str(getattr(self.bound_weapon, self.which_func)(self.constants))
    
class WeaponBar(MDBoxLayout, BoxSized, NeedsConstants):
    def __init__(self, **kwargs):
        super().__init__(
            orientation="horizontal",
            box_width = BOX_WIDTH,
            box_height = 2,
            **kwargs,
        )

        self.box_init()
        self.constants_init()

        self.weapon_icon = WPIcon()
        self.ammo = WPAmmoCount()
        self.damage = WPAttackOrDamage(which_func="damage")
        self.attack = WPAttackOrDamage(which_func="attack")
        self.ammo_type = WPAmmoType()
        self.spacer = Spacer(
            box_height=2,
            box_width=self.box_width - sum(
                [
                    self.weapon_icon.box_width,
                    self.ammo.box_width,
                    self.damage.box_width,
                    self.attack.box_width,
                ]
            )
        )

        self.add_widget(self.weapon_icon)
        self.add_widget(self.ammo)
        self.add_widget(self.ammo_type)
        self.add_widget(self.spacer)
        self.add_widget(self.attack)
        self.add_widget(self.damage)

class WPAmmoType(CenteredLabel, NeedsWeapon, TouchableMixin):
    def __init__(self, **kwargs):
        super().__init__(
            text="",
            box_width=1,
            box_height=2,
            **kwargs,
        )
        self.constants_init()
        self.weapons_init()
        self.touch_init()
        
    def weapon_changed(self, *args):
        super().weapon_changed(*args)
        if self.bound_weapon is not None:
            self.text = self.bound_weapon.loaded_ammo

    def weapon_modified(self, wep: "Weapon"):
        super().weapon_modified(wep)
        if self.bound_weapon is not None:
            self.text = self.bound_weapon.loaded_ammo

    def on_left_click(self, position):
        super().on_left_click(position)
        if self.bound_weapon is not None:
            self.bound_weapon.switch_ammo()
        
    




    

    