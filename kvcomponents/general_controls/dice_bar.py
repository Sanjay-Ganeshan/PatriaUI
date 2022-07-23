from ..shared.progressive_icon import ProgressiveIcon, ProgressiveText
from ..shared.box_sized_mixin import BoxSized
from ..shared.touchable_mixin import TouchableMixin
from ..shared.needs_character_mixin import NeedsConstants
from ..shared.spacer import Spacer
from kivymd.uix.boxlayout import MDBoxLayout

from ..resource_list import Resources
from ...models.dice import Dice, RollStatus, roll
from ...models.game import THE_GAME
from ...models.app_settings import BOX_WIDTH


class AnyDiceRoller(ProgressiveText, TouchableMixin, NeedsConstants):
    def __init__(self, **kwargs):
        n_faces = kwargs.pop("maximum_value")
        super().__init__(
            source=Resources.DICE_ICONS[n_faces],
            current_value=n_faces,
            maximum_value=n_faces,
            pr_full_color="coral",
            box_width=1,
            box_height=1,
            bold=True,
            text_color="white",
            theme_text_color="Custom",
            **kwargs,
        )
        self.touch_init()
        self.bind(maximum_value=self.adjust_sides)
        self.constants_init()

    def get_text(self) -> str:
        return str(self.maximum_value)

    def adjust_sides(self, *args):
        self.source = Resources.DICE_ICONS[self.maximum_value]
        self.current_value = self.maximum_value

    def on_left_click(self, *args):
        roll(Dice(self.maximum_value), description=f"{self.constants.CHARACTER_NAME} rolls")


class AdvantageRoll(ProgressiveIcon, TouchableMixin, NeedsConstants):
    def __init__(self, **kwargs):
        super().__init__(
            source=Resources.ADVANTAGE,
            current_value=0,
            maximum_value=1,
            pr_full_color="green",
            pr_empty_color="white",
            box_width=1,
            box_height=1,
            **kwargs,
        )
        self.touch_init()
        self.constants_init()

    def on_left_click(self, *args):
        if self.constants.NEXT_ROLL_STATUS == RollStatus.ADVANTAGE:
            THE_GAME.change_roll_status(
                RollStatus.STANDARD,
            )
        else:
            THE_GAME.change_roll_status(
                RollStatus.ADVANTAGE,
            )

    def adapt_to_constants(self, *args):
        super().adapt_to_constants(*args)
        self.tooltip_text = self.help_text.ADVANTAGE
        self.current_value = (
            1 if self.constants.NEXT_ROLL_STATUS == RollStatus.ADVANTAGE else 0
        )


class DisadvantageRoll(ProgressiveIcon, TouchableMixin, NeedsConstants):
    def __init__(self, **kwargs):
        super().__init__(
            source=Resources.DISADVANTAGE,
            current_value=0,
            maximum_value=1,
            pr_full_color="red",
            pr_empty_color="white",
            box_width=1,
            box_height=1,
            **kwargs,
        )
        self.touch_init()
        self.constants_init()

    def on_left_click(self, *args):
        if self.constants.NEXT_ROLL_STATUS == RollStatus.DISADVANTAGE:
            THE_GAME.change_roll_status(
                RollStatus.STANDARD,
            )
        else:
            THE_GAME.change_roll_status(
                RollStatus.DISADVANTAGE,
            )

    def adapt_to_constants(self, *args):
        super().adapt_to_constants(*args)
        self.tooltip_text = self.help_text.DISADVANTAGE
        self.current_value = (
            1 if self.constants.NEXT_ROLL_STATUS == RollStatus.DISADVANTAGE else 0
        )


class DiceBar(MDBoxLayout, BoxSized, NeedsConstants):
    def __init__(self, **kwargs):
        super().__init__(
            box_width=BOX_WIDTH,
            box_height=1,
            orientation="horizontal",
            **kwargs,
        )
        self.box_init()
        self.constants_init()
        self.d2 = AnyDiceRoller(maximum_value=2)
        self.d4 = AnyDiceRoller(maximum_value=4)
        self.d6 = AnyDiceRoller(maximum_value=6)
        self.d8 = AnyDiceRoller(maximum_value=8)
        self.d10 = AnyDiceRoller(maximum_value=10)
        self.d12 = AnyDiceRoller(maximum_value=12)
        self.d20 = AnyDiceRoller(maximum_value=20)
        self.adv = AdvantageRoll()
        self.disadv = DisadvantageRoll()
        self.lspace = Spacer(box_width=1.5, box_height=1)
        self.rspace = Spacer(box_width=1.5, box_height=1)

        self.add_widget(self.lspace)
        self.add_widget(self.disadv)
        self.add_widget(self.adv)
        self.add_widget(self.d2)
        self.add_widget(self.d4)
        self.add_widget(self.d6)
        self.add_widget(self.d8)
        self.add_widget(self.d10)
        self.add_widget(self.d12)
        self.add_widget(self.d20)
        self.add_widget(self.rspace)
