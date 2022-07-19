
from ..shared.centered_label import CenteredLabel
from ..shared.needs_character_mixin import NeedsConstants
from ..shared.progressive_icon import ProgressiveIconImpl
from kivy.properties import NumericProperty
from ..resource_list import Resources


class CHArmor(CenteredLabel, ProgressiveIconImpl, NeedsConstants):
    armor_rating = NumericProperty(0)

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

        self.text = self._get_label_text()
        self.tooltip_text = self._get_help_text()

        self.bind(armor_rating=self.on_armor_changed)

    def _get_label_text(self) -> str:
        return f"Armor\n{self.armor_rating}"

    def _get_help_text(self) -> str:
        return self.help_text.ARMOR

    def on_armor_changed(self, *args) -> None:
        self.text = self._get_label_text()
        self.tooltip_text = self._get_help_text()

    def adapt_to_constants(self, *args):
        super().adapt_to_constants(*args)
        self.armor_rating = self.constants.ARMOR_RATING
