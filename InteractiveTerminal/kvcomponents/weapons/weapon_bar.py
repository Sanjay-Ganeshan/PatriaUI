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
            self.tooltip_text = self.get_tooltip_text()

    def weapon_modified(self, wep):
        super().weapon_modified(wep)
        if self.bound_weapon is not None:
            self.current_value = self.bound_weapon.clip_current
            self.maximum_value = self.bound_weapon.clip_capacity
            self.text = self.get_text()
            self.tooltip_text = self.get_tooltip_text()

    def on_left_click(self, position):
        super().on_left_click(position)
        if self.bound_weapon is not None:
            self.bound_weapon.fire()
    
    def on_right_click(self, position):
        super().on_right_click(position)
        if self.bound_weapon is not None:
            self.bound_weapon.reload()

    def get_tooltip_text(self) -> str:
        if self.bound_weapon is None:
            return ""
        else:
            return (
                f"Loaded bullets: {self.bound_weapon.clip_current}x{self.bound_weapon.loaded_ammo}\n"
                f"Total Remaining Ammo (including bullets in active magazine): \n"
                + "\n".join((f"{ammo_type}: {self.bound_weapon.ammo_count[ammo_type][0]}" for ammo_type in sorted(self.bound_weapon.ammo_count)))
            )

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
        self.tooltip_text = (
            f"{wep.name}\n{wep.description}\nModifications: {', '.join([str(type(t).__name__) for t in wep.attachments])}\n"
            f"LClick - Change weapons, RClick - Fully resupply this weapon"
        )
    
    def on_left_click(self, position):
        super().on_left_click(position)
        THE_GAME.adjust_current_character(
            ACTIVE_WEAPON=((self.constants.ACTIVE_WEAPON + 1) % len(self.constants.WEAPONS))
        )
    
    def on_right_click(self, position):
        super().on_right_click(position)
        wep = self.constants.get_active_weapon()
        wep.restore()

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

class WPAttackOrDamageIcon(BoxSized, Image, TouchableMixin, NeedsWeapon, OptionalTooltip):
    def __init__(self, which_func, **kwargs):
        self.which_func = which_func
        super().__init__(
            source=Resources.BLOOD if self.which_func == "damage" else Resources.RETICLE,
            box_width=0.5,
            box_height=2,
            color="darkred",
            tooltip_text = "LClick - fire, RClick - roll, no ammo reduction",
            **kwargs
        )
        self.constants_init()
        self.weapons_init()
        self.touch_init()
    
    def on_left_click(self, position):
        super().on_left_click(position)
        if self.bound_weapon is not None and self.constants is not None:
            if self.which_func == "attack":
                fired = self.bound_weapon.fire()
            else:
                fired = True
            if fired:
                getattr(self.bound_weapon, self.which_func)(self.constants).roll()
            else:
                THE_GAME.game_log.log(f"{self.constants.CHARACTER_NAME} tries can't fire {self.bound_weapon.loaded_ammo} - clip is empty!")
    
    def on_right_click(self, position):
        super().on_right_click(position)
        # no ammo check
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
        self.weapon_common()

    
    def weapon_changed(self, *args):
        super().weapon_changed(*args)
        self.weapon_common()
    
    def weapon_common(self):
        if self.bound_weapon is None:
            self.dmg.text = ""
        else:
            roll_s = str(getattr(self.bound_weapon, self.which_func)(self.constants))
            self.dmg.text = roll_s

        
    
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
        self.mode_switcher = WPModeSwitcher()
        self.spacer = Spacer(
            box_height=2,
            box_width=self.box_width - sum(
                [
                    self.weapon_icon.box_width,
                    self.ammo.box_width,
                    self.damage.box_width,
                    self.attack.box_width,
                    self.mode_switcher.box_width,
                    self.ammo_type.box_width,
                ]
            )
        )

        self.add_widget(self.weapon_icon)
        self.add_widget(self.ammo)
        self.add_widget(self.ammo_type)
        self.add_widget(self.mode_switcher)
        self.add_widget(self.spacer)
        self.add_widget(self.attack)
        self.add_widget(self.damage)

class WPAmmoType(CenteredLabel, NeedsWeapon, TouchableMixin):
    def __init__(self, **kwargs):
        super().__init__(
            text="",
            box_width=1,
            box_height=2,
            font_style="Body1",
            **kwargs,
        )
        self.constants_init()
        self.weapons_init()
        self.touch_init()
        
    def weapon_changed(self, *args):
        super().weapon_changed(*args)
        self.weapon_common()

    def weapon_modified(self, wep: "Weapon"):
        super().weapon_modified(wep)
        self.weapon_common()
    
    def weapon_common(self):
        if self.bound_weapon is not None:
            ammo_pref = f"Firing {self.bound_weapon.allowed_burst_sizes[self.bound_weapon.burst_size_ix]}x {self.bound_weapon.loaded_ammo}"
            cal_suff = f"{self.bound_weapon.caliber} cal @ {self.bound_weapon.range_meters}m"
            self.text = f"{ammo_pref}\n{cal_suff}"
        else:
            self.text = "N/A"
        self.bound_weapon.loaded_ammo
        self.tooltip_text = self.get_tooltip_text()

    def on_left_click(self, position):
        super().on_left_click(position)
        if self.bound_weapon is not None:
            self.bound_weapon.switch_ammo()
    
    def on_right_click(self, position):
        super().on_right_click(position)
        if self.bound_weapon is not None:
            self.bound_weapon.switch_burst()
        
    def get_tooltip_text(self) -> str:
        if self.bound_weapon is None:
            return ""
        else:
            return (
                f"Available ammo types: {sorted(self.bound_weapon.ammo_count.keys())}\n"
                f"Available burst size: {sorted(self.bound_weapon.allowed_burst_sizes)}\n"
                f"LClick: change ammo, RClick: change burst size\n"
                f"Hover over ammo count to see counts for each."
            )

class WPModeSwitcher(CenteredLabel, NeedsWeapon, TouchableMixin):
    def __init__(self, **kwargs):
        super().__init__(
            text="",
            box_width=1,
            box_height=2,
            font_style="Body1",
            **kwargs,
        )
        self.constants_init()
        self.weapons_init()
        self.touch_init()
        
    def weapon_changed(self, *args):
        super().weapon_changed(*args)
        self.weapon_common()

    def weapon_modified(self, wep: "Weapon"):
        super().weapon_modified(wep)
        self.weapon_common()
    
    def weapon_common(self):
        if self.bound_weapon is not None:
            self.text = f"Mode: {self.bound_weapon.get_current_mode()}"
        else:
            self.text = "N/A"
        self.tooltip_text = self.get_tooltip_text()

    def on_left_click(self, position):
        super().on_left_click(position)
        if self.bound_weapon is not None:
            self.bound_weapon.switch_mode()
    
        
    def get_tooltip_text(self) -> str:
        if self.bound_weapon is None:
            return ""
        else:
            return (
                f"Allowed modes: {sorted(self.bound_weapon.allowed_modes)}\n"
                f"LClick: change mode"
            )


    

    