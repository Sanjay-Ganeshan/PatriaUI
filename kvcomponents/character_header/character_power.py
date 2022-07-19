from ..shared.box_sized_mixin import BoxSizedBoxLayout, BoxSized
from ..shared.progressive_icon import ProgressiveIcon
from ..shared.needs_character_mixin import NeedsConstants
from ..shared.touchable_mixin import TouchableMixin
from ..shared.centered_label import CenteredLabel
from kivymd.uix.boxlayout import MDBoxLayout

from ..resource_list import Resources

from ...models.dice import Dice, roll
from ...models.game import THE_GAME


class SkinSuitPowerIcon(ProgressiveIcon, NeedsConstants, TouchableMixin):
    """
    Skinsuit Progressive Icon
    """

    def __init__(self, **kwargs):
        super().__init__(
            source=Resources.SKINSUIT_ICON,
            current_value=0,
            maximum_value=1,
            pr_empty_color="black",
            pr_full_color="blue",
            **kwargs,
        )
        self.constants_init()
        self.touch_init()

        self.tooltip_text = self.help_text.SUIT

    def adapt_to_constants(self, *args):
        super().adapt_to_constants(*args)
        self.current_value = self.constants.SUIT_POWER
        self.maximum_value = self.constants.SUIT_CAPACITY
        self.tooltip_text = self.help_text.SUIT

    def on_left_click(self, *args):
        super().on_left_click(*args)
        new_value = max(0, self.current_value - 1)
        THE_GAME.adjust_current_character(
            SUIT_POWER=new_value,
        )

    def on_right_click(self, *args):
        super().on_right_click(*args)
        new_value = min(self.current_value + 2, self.maximum_value)
        THE_GAME.adjust_current_character(
            SUIT_POWER=new_value,
        )


class ShieldPowerIcon(ProgressiveIcon, NeedsConstants, TouchableMixin):
    """
    Shield Power stacked progressive icon
    """

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
        self.constants_init()
        self.touch_init()

        self.tooltip_text = self.help_text.SHIELD

    def adapt_to_constants(self, *args):
        super().adapt_to_constants()
        self.current_value = self.constants.SHIELD_POWER
        self.maximum_value = self.constants.SHIELD_CAPACITY
        self.tooltip_text = self.help_text.SHIELD

    def on_left_click(self, *args):
        super().on_left_click(*args)
        new_value = max(0, self.current_value - 1)
        THE_GAME.adjust_current_character(
            SHIELD_POWER=new_value,
        )

    def on_right_click(self, *args):
        super().on_right_click(*args)
        replenishment, _ = roll(
            Dice.D2,
            description=(
                f"{self.constants.CHARACTER_NAME} replenishes "
                f"{self.constants.PRONOUN_HER} shields"
            ),
        )
        new_value = min(self.current_value + replenishment, self.maximum_value)
        THE_GAME.adjust_current_character(
            SHIELD_POWER=new_value,
        )


class CHPower(MDBoxLayout, BoxSized, NeedsConstants):
    """
    Skinsuit and Shield Power
    """

    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", box_width=2, box_height=3, **kwargs)
        self.box_init()
        self.constants_init()
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

    def adapt_to_constants(self, *args):
        super().adapt_to_constants(*args)
        self.charge_suit.text = (
            f"{self.constants.SUIT_POWER} / {self.constants.SUIT_CAPACITY}"
        )
        self.charge_shield.text = (
            f"{self.constants.SHIELD_POWER} / {self.constants.SHIELD_CAPACITY}"
        )
