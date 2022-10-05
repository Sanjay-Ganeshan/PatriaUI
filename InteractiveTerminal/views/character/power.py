from kivy.properties import NumericProperty
from kivymd.uix.boxlayout import MDBoxLayout

from ...new_models.character.character import Character
from ...new_models.character.status import Status
from ...new_models.events.ev_base import GameOrViewEvent
from ...new_models.events.game_events import (ConsumeShield,
                                              ConsumeSkinsuitCharge,
                                              RestoreShield,
                                              RestoreSkinsuitCharge)
from ...new_models.help import help_generator
from ...new_models.state.state_manager import StateManager
from ..resource_list import Resources
from ..shared.box_sized_mixin import BoxSized, BoxSizedBoxLayout
from ..shared.centered_label import CenteredLabel
from ..shared.listens_for_state_changes import ListenForStateChanges
from ..shared.progressive_icon import ProgressiveIcon
from ..shared.touchable_mixin import TouchableMixin


class SkinSuitPowerIcon(ProgressiveIcon, TouchableMixin, ListenForStateChanges):
    """
    Skinsuit Progressive Icon
    """

    current_power: int = NumericProperty(0)
    max_power: int = NumericProperty(1)

    def __init__(self, **kwargs):
        super().__init__(
            source=Resources.SKINSUIT_ICON,
            current_value=0,
            maximum_value=1,
            pr_empty_color="black",
            pr_full_color="blue",
            **kwargs,
        )
        self.touch_init()
        self.listener_init()

        self.bind(current_power=self.power_updated, max_power=self.power_updated)

    def power_updated(self, *args):
        self.current_value = self.current_power
        self.maximum_value = self.max_power
        self.tooltip_text = help_generator.suit(self.current_power)

    def listener(
        self, ev: GameOrViewEvent, is_forward: bool, state_manager: StateManager
    ) -> None:
        # No reason to filter events, kivy will figure things out when we set properties

        # We might have changed the current character's icon. Look it up
        if state_manager.view_state.focused_character is None:
            self.current_power = 0
            self.max_power = 1
        else:
            char: Character = state_manager.game_state.characters[
                state_manager.view_state.focused_character
            ]
            current: Status = char.current_life
            maxi: Status = char.max_life

            self.current_power = current.suit_power
            self.max_power = maxi.suit_power

    def on_left_click(self, *args):
        super().on_left_click(*args)
        if self.state_manager is None:
            return

        if self.state_manager.view_state.focused_character is None:
            return

        # Left click -> Consume a skinsuit charge
        self.state_manager.push_event(
            ConsumeSkinsuitCharge(
                character_id=self.state_manager.view_state.focused_character
            )
        )

    def on_right_click(self, *args):
        super().on_right_click(*args)

        if self.state_manager is None:
            return

        if self.state_manager.view_state.focused_character is None:
            return

        self.state_manager.push_event(
            RestoreSkinsuitCharge(
                character_id=self.state_manager.view_state.focused_character
            )
        )


class ShieldPowerIcon(ProgressiveIcon, TouchableMixin, ListenForStateChanges):
    """
    Shield Power stacked progressive icon
    """

    current_shield: int = NumericProperty(0)
    max_shield: int = NumericProperty(1)

    def __init__(self, **kwargs):
        super().__init__(
            source=Resources.ENERGY_SHIELD_ICON,
            current_value=0,
            maximum_value=1,
            pr_empty_color="black",
            pr_full_color="blue",
            stacked=True,
            orientation="horizontal",
            **kwargs,
        )
        self.touch_init()
        self.listener_init()

        self.bind(current_shield=self.shield_updated, max_shield=self.shield_updated)

    def shield_updated(self, *args):
        self.current_value = self.current_shield
        self.maximum_value = self.max_shield
        self.tooltip_text = help_generator.shield(
            shield_power=self.current_shield, shield_capacity=self.max_shield
        )

    def listener(
        self, ev: GameOrViewEvent, is_forward: bool, state_manager: StateManager
    ) -> None:
        # No reason to filter events, kivy will figure things out when we set properties

        # We might have changed the current character's icon. Look it up
        if state_manager.view_state.focused_character is None:
            self.current_shield = 0
            self.max_shield = 1
        else:
            char: Character = state_manager.game_state.characters[
                state_manager.view_state.focused_character
            ]
            current: Status = char.current_life
            maxi: Status = char.max_life

            self.current_shield = current.shield_power
            self.max_shield = maxi.shield_power

    def on_left_click(self, *args):
        super().on_left_click(*args)
        if self.state_manager is None:
            return

        if self.state_manager.view_state.focused_character is None:
            return

        # Left click -> Consume a skinsuit charge
        self.state_manager.push_event(
            ConsumeShield(character_id=self.state_manager.view_state.focused_character)
        )

    def on_right_click(self, *args):
        super().on_right_click(*args)

        if self.state_manager is None:
            return

        if self.state_manager.view_state.focused_character is None:
            return

        self.state_manager.push_event(
            RestoreShield(character_id=self.state_manager.view_state.focused_character)
        )


class CHPower(MDBoxLayout, BoxSized, ListenForStateChanges):
    """
    Skinsuit and Shield Power
    """

    suit_power: int = NumericProperty(0)
    suit_capacity: int = NumericProperty(1)
    shield_power: int = NumericProperty(0)
    shield_capacity: int = NumericProperty(1)

    def __init__(self, **kwargs):
        super().__init__(
            orientation="vertical",
            box_width=2,
            box_height=3,
            **kwargs,
        )
        self.box_init()
        self.listener_init()
        self.lbl_suit = CenteredLabel(
            text="Suit",
            box_height=0.75,
            box_width=1,
        )
        self.lbl_shield = CenteredLabel(
            text="Shield",
            box_height=0.75,
            box_width=1,
        )
        self.lbl_box = BoxSizedBoxLayout(
            orientation="horizontal",
            box_width=2,
            box_height=0.75,
        )
        self.lbl_box.add_widget(self.lbl_suit)
        self.lbl_box.add_widget(self.lbl_shield)

        self.img_suit = SkinSuitPowerIcon(
            box_height=1,
            box_width=1,
        )
        self.img_shield = ShieldPowerIcon(
            box_height=1,
            box_width=1,
        )

        self.img_box = BoxSizedBoxLayout(
            orientation="horizontal",
            box_width=2,
            box_height=1,
        )
        self.img_box.add_widget(self.img_suit)
        self.img_box.add_widget(self.img_shield)

        self.charge_suit = CenteredLabel(
            text="",
            box_height=0.75,
            box_width=1,
        )
        self.charge_shield = CenteredLabel(
            text="",
            box_height=0.75,
            box_width=1,
        )
        self.charge_box = BoxSizedBoxLayout(
            orientation="horizontal",
            box_width=2,
            box_height=0.75,
        )
        self.charge_box.add_widget(self.charge_suit)
        self.charge_box.add_widget(self.charge_shield)

        self.add_widget(self.lbl_box)
        self.add_widget(self.img_box)
        self.add_widget(self.charge_box)

        self.bind(
            suit_power=self.update_text,
            suit_capacity=self.update_text,
            shield_power=self.update_text,
            shield_capacity=self.update_text,
        )
        
        self.update_text()

    def update_text(self, *args):
        self.charge_suit.text = (
            f"{self.suit_power} / {self.suit_capacity}"
        )
        self.charge_shield.text = (
            f"{self.shield_power} / {self.shield_capacity}"
        )

    def listener(
        self, ev: GameOrViewEvent, is_forward: bool, state_manager: StateManager
    ) -> None:
        # No reason to filter events, kivy will figure things out when we set properties

        # We might have changed the current character's icon. Look it up
        if state_manager.view_state.focused_character is None:
            self.shield_power = 0
            self.shield_capacity = 1
            self.suit_power = 0
            self.suit_capacity = 1
        else:
            char: Character = state_manager.game_state.characters[
                state_manager.view_state.focused_character
            ]
            current: Status = char.current_life
            maxi: Status = char.max_life

            self.shield_power = current.shield_power
            self.shield_capacity = maxi.shield_power
            self.suit_power = current.suit_power
            self.suit_capacity = maxi.suit_power
