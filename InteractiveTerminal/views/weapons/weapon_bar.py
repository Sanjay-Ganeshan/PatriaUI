import typing as T

from kivy.properties import (
    BooleanProperty, NumericProperty, ObjectProperty, StringProperty
)
from kivy.uix.image import Image
from kivymd.uix.boxlayout import MDBoxLayout

from ...new_models.character.character import Character
from ...new_models.dice.rolls import Roll
from ...new_models.events.ev_base import GameOrViewEvent
from ...new_models.events.game_events import (
    AttackOrDamageCurrentWeapon, ChangeWeaponAmmo, ChangeWeaponBurst,
    ChangeWeaponMode, ChangeWeapons, FireCurrentWeapon, ReloadCurrentWeapon,
    ResupplyWeapon
)
from ...new_models.help import help_generator
from ...new_models.state.app_settings import BOX_WIDTH
from ...new_models.state.state_manager import StateManager
from ..resource_list import Resources
from ..shared.box_sized_mixin import BoxSized
from ..shared.centered_label import CenteredLabel
from ..shared.listens_for_state_changes import ListenForStateChanges
from ..shared.progressive_icon import ProgressiveText
from ..shared.spacer import Spacer
from ..shared.tooltip import OptionalTooltip
from ..shared.touchable_mixin import TouchableMixin


class WPAmmoCount(ProgressiveText, ListenForStateChanges, TouchableMixin):
    """
    Reload + consume ammo
    """

    clip_current: int = NumericProperty(1)
    clip_capacity: int = NumericProperty(2)
    total_ammo: int = NumericProperty(10)
    burst_size: int = NumericProperty(1)

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

        self.touch_init()
        self.listener_init()

        self.bind(
            clip_current=self.ammo_updated,
            clip_capacity=self.ammo_updated,
            burst_size=self.ammo_updated,
            total_ammo=self.ammo_updated,
        )

    def ammo_updated(self, *args) -> None:
        self.current_value = self.clip_current
        self.maximum_value = self.clip_capacity

        if self.clip_current < self.burst_size:
            self.pr_full_color = "darkred"
        else:
            self.pr_full_color = "gold"

        self.text = self.get_text()

    def on_left_click(self, position):
        super().on_left_click(position)
        if self.state_manager is None:
            return

        if self.state_manager.view_state.focused_character is None:
            return

        self.state_manager.push_event(
            FireCurrentWeapon(
                character_id=self.state_manager.view_state.focused_character
            )
        )

    def on_right_click(self, position):
        super().on_right_click(position)
        if self.state_manager is None:
            return

        if self.state_manager.view_state.focused_character is None:
            return

        self.state_manager.push_event(
            ReloadCurrentWeapon(
                character_id=self.state_manager.view_state.focused_character
            )
        )

    def get_text(self):
        """
        Get the text
        "{loaded} / {clip size} ({remaining unloaded ammo of this type})"
        """
        return f"{self.clip_current} / {self.clip_capacity} ({self.total_ammo - self.clip_current})"

    def listener(
        self, ev: GameOrViewEvent, is_forward: bool, state_manager: StateManager
    ) -> None:
        use_defaults: bool = True
        if state_manager.view_state.focused_character is not None:
            char = state_manager.game_state.characters[
                state_manager.view_state.focused_character]
            weapon = char.weapons.get()
            if weapon is not None:
                use_defaults = False
                self.clip_current = weapon.clip_current
                self.clip_capacity = weapon.clip_capacity

                ammo = weapon.ammo.get()
                if ammo is not None:
                    self.total_ammo = ammo.current
                else:
                    self.total_ammo = weapon.clip_current

                if weapon.burst.get() is not None:
                    self.burst_size = weapon.burst.get()
                else:
                    self.burst_size = 0

        if use_defaults:
            self.clip_current = 0
            self.clip_capacity = 1
            self.total_ammo = 1
            self.burst_size = 1


class WPIcon(
    Image, BoxSized, ListenForStateChanges, TouchableMixin, OptionalTooltip
):
    weapon_name: str = StringProperty("")
    weapon_description: str = StringProperty("")
    weapon_attachment_names: T.Optional[T.List[str]
                                       ] = ObjectProperty(None, allownone=True)

    weapon_shortname: str = StringProperty("")

    def __init__(self, **kwargs):
        super().__init__(
            source="",
            box_width=3,
            box_height=2,
            allow_stretch=True,
            **kwargs,
        )
        self.box_init()
        self.touch_init()
        self.listener_init()

        self.bind(
            weapon_name=self.desc_changed,
            weapon_description=self.desc_changed,
            weapon_attachment_names=self.desc_changed
        )
        self.bind(weapon_shortname=self.shortname_changed)

    def desc_changed(self, *args):
        self.tooltip_text = help_generator.weapon(
            self.weapon_name, self.weapon_description,
            self.weapon_attachment_names
        )

    def shortname_changed(self, *args):
        self.source = Resources.WEAPON_ICONS.get(
            self.weapon_shortname,
            Resources.MISSING,
        )

    def listener(
        self, ev: GameOrViewEvent, is_forward: bool, state_manager: StateManager
    ) -> None:
        use_defaults: bool = True
        if state_manager.view_state.focused_character is not None:
            char = state_manager.game_state.characters[
                state_manager.view_state.focused_character]
            weapon = char.weapons.get()
            if weapon is not None:
                use_defaults = False
                self.weapon_name = weapon.name
                self.weapon_attachment_names = [
                    a.get_name() for a in weapon.attachments
                ]
                self.weapon_shortname = weapon.short_name
                self.weapon_description = weapon.description

        if use_defaults:
            self.weapon_name = "<long name>"
            self.weapon_attachment_names = None
            self.weapon_shortname = "<short name>"
            self.weapon_description = "<description>"

    def on_left_click(self, position):
        super().on_left_click(position)
        if self.state_manager is None:
            return

        if self.state_manager.view_state.focused_character is None:
            return

        self.state_manager.push_event(
            ChangeWeapons(
                character_id=self.state_manager.view_state.focused_character
            )
        )

    def on_right_click(self, position):
        super().on_right_click(position)
        if self.state_manager is None:
            return

        if self.state_manager.view_state.focused_character is None:
            return

        self.state_manager.push_event(
            ResupplyWeapon(
                character_id=self.state_manager.view_state.focused_character
            )
        )


class WPWeaponName(CenteredLabel, ListenForStateChanges, TouchableMixin):
    weapon_short_name: str = StringProperty("<name>")

    def __init__(self, **kwargs):
        super().__init__(
            text="ttt",
            box_width=2,
            box_height=2,
            **kwargs,
        )

        self.listener_init()
        self.bind(weapon_short_name=self.short_name_changed)

    def short_name_changed(self, *args):
        self.text = self.weapon_short_name

    def listener(
        self, ev: GameOrViewEvent, is_forward: bool, state_manager: StateManager
    ) -> None:
        use_defaults: bool = True
        if state_manager.view_state.focused_character is not None:
            char = state_manager.game_state.characters[
                state_manager.view_state.focused_character]
            weapon = char.weapons.get()
            if weapon is not None:
                use_defaults = False
                self.weapon_short_name = weapon.short_name

        if use_defaults:
            self.weapon_short_name = "<short name>"


class WPAttackOrDamageIcon(
    BoxSized, Image, TouchableMixin, ListenForStateChanges, OptionalTooltip
):
    is_attack: bool = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(
            source=Resources.MISSING,
            box_width=0.5,
            box_height=2,
            color="darkred",
            tooltip_text="LClick - fire, RClick - roll, no ammo reduction",
            **kwargs
        )
        self.touch_init()
        self.bind(is_attack=self.is_attack_updated)
        self.is_attack_updated()
        self.listener_init()

    def is_attack_updated(self, *args) -> None:
        self.source = Resources.RETICLE if self.is_attack else Resources.BLOOD

    def on_left_click(self, position):
        super().on_left_click(position)
        self.common_click(True)

    def common_click(self, is_left: bool):
        if self.state_manager is None:
            return

        if self.state_manager.view_state.focused_character is None:
            return

        char_id = self.state_manager.view_state.focused_character

        events = []
        if is_left and self.is_attack:
            events.append(FireCurrentWeapon(character_id=char_id))
        events.append(
            AttackOrDamageCurrentWeapon(
                character_id=char_id, is_attack=self.is_attack
            )
        )
        self.state_manager.push_event(events)

    def on_right_click(self, position):
        super().on_right_click(position)
        self.common_click(False)


class WPAttackOrDamage(MDBoxLayout, BoxSized, ListenForStateChanges):
    is_attack: bool = BooleanProperty(False)
    attack_roll: T.Optional[Roll] = ObjectProperty(None, allownone=True)
    dmg_roll: T.Optional[Roll] = ObjectProperty(None, allownone=True)

    def __init__(self, **kwargs):
        super().__init__(
            **kwargs,
            orientation="horizontal",
            box_width=2.5,
            box_height=2,
        )
        self.box_init()
        self.listener_init()

        self.icon = WPAttackOrDamageIcon(is_attack=self.is_attack)
        self.dmg = CenteredLabel(
            box_width=2, box_height=2, halign="left", font_style="H5"
        )

        self.add_widget(self.icon)
        self.add_widget(self.dmg)

        self.bind(
            is_attack=self.roll_updated,
            attack_roll=self.roll_updated,
            dmg_roll=self.roll_updated
        )
        self.roll_updated()

    def roll_updated(self, *args):
        self.icon.is_attack = self.is_attack

        roll = self.attack_roll if self.is_attack else self.dmg_roll

        if roll is None:
            self.dmg.text = "--"
        else:
            self.dmg.text = str(roll)

    def listener(
        self, ev: GameOrViewEvent, is_forward: bool, state_manager: StateManager
    ) -> None:
        use_defaults: bool = True
        if state_manager.view_state.focused_character is not None:
            char = state_manager.game_state.characters[
                state_manager.view_state.focused_character]
            weapon = char.weapons.get()
            if weapon is not None:
                use_defaults = False
                self.attack_roll = weapon.attack(char.stat_block)
                self.dmg_roll = weapon.damage(char.stat_block)

        if use_defaults:
            self.attack_roll = None
            self.dmg_roll = None


class WeaponBar(MDBoxLayout, BoxSized, ListenForStateChanges):
    def __init__(self, **kwargs):
        super().__init__(
            orientation="horizontal",
            box_width=BOX_WIDTH,
            box_height=2,
            **kwargs,
        )

        self.box_init()
        self.listener_init()

        self.weapon_icon = WPIcon()
        self.ammo = WPAmmoCount()
        self.damage = WPAttackOrDamage(is_attack=False)
        self.attack = WPAttackOrDamage(is_attack=True)
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


class WPAmmoType(CenteredLabel, ListenForStateChanges, TouchableMixin):
    burst_size: T.Optional[int] = ObjectProperty(None, allownone=True)
    ammo_name: T.Optional[str] = ObjectProperty(None, allownone=True)
    caliber: T.Optional[float] = ObjectProperty(None, allownone=True)
    range_m: T.Optional[int] = ObjectProperty(None, allownone=True)
    splash: T.Optional[int] = ObjectProperty(None, allownone=True)

    available_ammo: T.Optional[T.List[str]
                              ] = ObjectProperty(None, allownone=True)
    available_burst: T.Optional[T.List[int]
                               ] = ObjectProperty(None, allownone=True)

    def __init__(self, **kwargs):
        super().__init__(
            text="",
            box_width=1,
            box_height=2,
            font_style="Body1",
            **kwargs,
        )
        self.touch_init()
        self.listener_init()

        self.bind(
            burst_size=self.update,
            ammo_name=self.update,
            caliber=self.update,
            range_m=self.update,
        )
        self.bind(
            available_ammo=self.update_help, available_burst=self.update_help
        )
        self.update()
        self.update_help()

    def listener(
        self, ev: GameOrViewEvent, is_forward: bool, state_manager: StateManager
    ) -> None:
        use_defaults: bool = True
        if state_manager.view_state.focused_character is not None:
            char = state_manager.game_state.characters[
                state_manager.view_state.focused_character]
            weapon = char.weapons.get()
            if weapon is not None:
                use_defaults = False

                self.burst_size = weapon.burst.get()
                self.caliber = weapon.caliber
                self.range_m = weapon.range_meters
                self.splash = weapon.splash_meters
                current_ammo = weapon.ammo.get()
                if current_ammo is None:
                    self.ammo_name = None
                else:
                    self.ammo_name = current_ammo.name
                self.available_ammo = [a.name for a in weapon.ammo]
                self.available_burst = list(iter(weapon.burst))

        if use_defaults:
            self.burst_size = None
            self.ammo_name = None
            self.caliber = None
            self.range_m = None
            self.splash = None

            self.available_ammo = None
            self.available_burst = None

    def update(self, *args):
        if self.burst_size is not None:
            burst_add = f"{self.burst_size}x "
        else:
            burst_add = ""
        if self.ammo_name is not None:
            ammo_add = f"{self.ammo_name}"
        else:
            ammo_add = f"?"

        if self.caliber is not None:
            cal_add = f"{self.caliber:.1f} cal "
        else:
            cal_add = ""

        if self.range_m is not None:
            range_add = f" {self.range_m}m"
        else:
            range_add = ""

        if self.splash is not None:
            splash_add = f"({self.splash}m AoE)"
        else:
            splash_add = ""

        prefix = f"{burst_add} {ammo_add}"
        suffix = f"{cal_add}{range_add}{splash_add}"
        self.text = f"{prefix}\n{suffix}"

    def update_help(self, *args) -> str:
        self.tooltip_text = help_generator.ammo_and_burst(
            self.available_ammo, self.available_burst
        )

    def on_left_click(self, position):
        super().on_left_click(position)
        if self.state_manager is None:
            return

        if self.state_manager.view_state.focused_character is None:
            return

        self.state_manager.push_event(
            ChangeWeaponAmmo(
                character_id=self.state_manager.view_state.focused_character
            )
        )

    def on_right_click(self, position):
        super().on_right_click(position)
        if self.state_manager is None:
            return

        if self.state_manager.view_state.focused_character is None:
            return

        self.state_manager.push_event(
            ChangeWeaponBurst(
                character_id=self.state_manager.view_state.focused_character
            )
        )


class WPModeSwitcher(CenteredLabel, ListenForStateChanges, TouchableMixin):
    mode_name: T.Optional[str] = ObjectProperty(None, allownone=True)
    allowed_modes: T.Optional[T.List[str]
                             ] = ObjectProperty(None, allownone=True)

    def __init__(self, **kwargs):
        super().__init__(
            text="",
            box_width=1,
            box_height=2,
            font_style="Body1",
            **kwargs,
        )
        self.touch_init()
        self.listener_init()
        self.bind(mode_name=self.update, allowed_modes=self.update)

    def update(self, *args):
        if self.mode_name is None:
            self.text = "N/A"
        else:
            self.text = f"Mode: {self.mode_name}"
        self.tooltip_text = help_generator.weapon_mode(self.allowed_modes)

    def on_left_click(self, position):
        super().on_left_click(position)
        if self.state_manager is None:
            return

        if self.state_manager.view_state.focused_character is None:
            return

        self.state_manager.push_event(
            ChangeWeaponMode(
                character_id=self.state_manager.view_state.focused_character
            )
        )

    def listener(
        self, ev: GameOrViewEvent, is_forward: bool, state_manager: StateManager
    ) -> None:
        use_defaults: bool = True
        if state_manager.view_state.focused_character is not None:
            char = state_manager.game_state.characters[
                state_manager.view_state.focused_character]
            weapon = char.weapons.get()
            if weapon is not None:
                use_defaults = False
                self.mode_name = weapon.mode.get()
                self.allowed_modes = [m for m in weapon.mode]

        if use_defaults:
            self.burst_size = None
            self.ammo_name = None
            self.caliber = None
            self.range = None

            self.available_ammo = None
            self.available_burst = None
