from kivymd.uix.boxlayout import MDBoxLayout
from ..shared.box_sized_mixin import BoxSized
from ..shared.needs_character_mixin import NeedsConstants
from ..shared.progressive_icon import ProgressiveIcon
from ..resource_list import Resources

class CHRestoration(MDBoxLayout, BoxSized, NeedsConstants):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", box_width=2, box_height=3, **kwargs)
        self.box_init()
        self.constants_init()

        self.deflections = ProgressiveIcon(
            box_width=2,
            box_height=1,
            source=Resources.DEFLECTION,
            stacked=True,
            current_value=0,
            maximum_value=1,
            pr_empty_color="black",
            pr_full_color="blue",
            orientation="horizontal",
        )

        self.revivals = ProgressiveIcon(
            box_width=2,
            box_height=1,
            source=Resources.REVIVAL,
            stacked=True,
            current_value=0,
            maximum_value=1,
            pr_empty_color="black",
            pr_full_color="green",
            orientation="horizontal",
        )

        self.hit_dice = ProgressiveIcon(
            box_width=2,
            box_height=1,
            source=Resources.HIT_DICE,
            stacked=True,
            current_value=0,
            maximum_value=1,
            pr_empty_color="black",
            pr_full_color="red",
            orientation="horizontal",
        )

        self.add_widget(self.deflections)
        self.add_widget(self.revivals)
        self.add_widget(self.hit_dice)

    def adapt_to_constants(self, *args):
        super().adapt_to_constants(*args)
        helpt = self.help_text

        self.deflections.tooltip_text = helpt.DEFLECT
        self.revivals.tooltip_text = helpt.REVIVAL
        self.hit_dice.tooltip_text = helpt.HIT_DICE

        self.deflections.current_value = self.constants.CURRENT_DEFLECTS
        self.deflections.maximum_value = self.constants.MAX_DEFLECTS
        self.revivals.current_value = self.constants.CURRENT_REVIVES
        self.revivals.maximum_value = self.constants.MAX_REVIVES
        self.hit_dice.current_value = self.constants.CURRENT_HIT_DICE
        self.hit_dice.maximum_value = self.constants.MAX_HIT_DICE
