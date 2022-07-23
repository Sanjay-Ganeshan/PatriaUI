from ..shared.centered_label import CenteredLabel
from ..shared.progressive_icon import ProgressiveIconImpl
from ..shared.needs_character_mixin import NeedsConstants
from ..shared.touchable_mixin import TouchableMixin

from ..resource_list import Resources
from ...models.dice import Dice, roll


from kivy.properties import (
    StringProperty,
    NumericProperty,
)

class StatDesignation(CenteredLabel, ProgressiveIconImpl, NeedsConstants, TouchableMixin):
    """
    A box displaying a single stat
    """

    stat_name = StringProperty("FILLME")
    stat_modifier = NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__(
            text="",
            font_style="H6",
            tooltip_text="",
            box_width=kwargs.pop("box_width", 2),
            box_height=kwargs.pop("box_height", 2),
            source=kwargs.pop("source", Resources.STAT_ICON),
            current_value=1,
            maximum_value=1,
            stacked=False,
            orientation="vertical",
            pr_full_color=kwargs.pop("pr_full_color", "black"),
            pr_empty_color="black",
            **kwargs,
        )
        self.progressive_init()
        self.box_init()
        self.constants_init()
        self.touch_init()

        self.text = self._get_label_string()
        self.tooltip_text = self.help_text.STAT_DESCRIPTIONS[self.stat_name]

        self.bind(stat_name=self.on_stats_changed, stat_modifier=self.on_stats_changed)

    def _get_label_string(self) -> str:
        return self.stat_name.split("_")[0] + "\n" + ("%+d" % self.stat_modifier)

    def on_stats_changed(self, *args):
        self.text = self._get_label_string()
        self.tooltip_text = self.help_text.STAT_DESCRIPTIONS[self.stat_name]

    def adapt_to_constants(self, *args):
        super().adapt_to_constants(*args)

        self.stat_modifier = getattr(self.constants, f"S_{self.stat_name}")

    def on_left_click(self, *args):
        super().on_left_click(*args)
        roll(
            Dice.D20,
            description=(
                f"{self.constants.CHARACTER_NAME} rolls {self.stat_name}"
            ),
            modifier=self.stat_modifier,
        )