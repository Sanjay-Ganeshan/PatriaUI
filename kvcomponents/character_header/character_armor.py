
from ..shared.centered_label import CenteredLabel
from ..shared.needs_character_mixin import NeedsConstants
from ..shared.touchable_mixin import TouchableMixin
from ..shared.progressive_icon import ProgressiveIconImpl
from kivy.properties import NumericProperty
from ..resource_list import Resources

from ...models.game import THE_GAME

class CHArmor(CenteredLabel, ProgressiveIconImpl, NeedsConstants, TouchableMixin):
    def __init__(self, **kwargs):
        """
        Displays your armor rating prominently
        """
        super().__init__(
            # Sizing
            box_height=3,
            box_width=1.5,
            # Centered Text
            text="",
            # Icon in back
            source=Resources.ARMOR_ICON,
            maximum_value=1,
            current_value=1,
            pr_empty_color="white",
            pr_full_color=kwargs.pop("pr_full_color", "white"),
            stacked=False,
            **kwargs,
        )
        self.constants_init()
        self.progressive_init()
        self.touch_init()


    def _get_label_text(self) -> str:
        if self.constants.ARMOR_BONUS > 0:
            armor_rating_txt = f"{self.constants.ARMOR_RATING}+{self.constants.ARMOR_BONUS}"
        else:
            armor_rating_txt = f"{self.constants.ARMOR_RATING}"
        return f"Armor\n{armor_rating_txt}"

    def _get_help_text(self) -> str:
        return self.help_text.ARMOR


    def adapt_to_constants(self, *args):
        super().adapt_to_constants(*args)
        self.text = self._get_label_text()
        self.tooltip_text = self._get_help_text()

    def on_left_click(self, *args):
        super().on_left_click(*args)
        # Left click -> Skinsuit
        if self.constants.SUIT_POWER > 0 and self.constants.ARMOR_BONUS == 0:
            new_power = self.constants.SUIT_POWER - 1
            new_armor_bonus = self.constants.ARMOR_BONUS + 3
            THE_GAME.adjust_current_character(
                SUIT_POWER = new_power,
                ARMOR_BONUS = new_armor_bonus,
            )
            THE_GAME.game_log.log(
                f"{self.constants.CHARACTER_NAME} uses a skinsuit charge "
                f"to bolster {self.constants.PRONOUN_HER} defense."
            )

    def on_right_click(self, *args):
        super().on_right_click(*args)
        THE_GAME.adjust_current_character(
            ARMOR_BONUS = 0,
        )