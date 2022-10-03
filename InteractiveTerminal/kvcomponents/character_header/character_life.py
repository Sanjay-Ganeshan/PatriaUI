from ...models.roll_status import RollStatus
from ..shared.progressive_icon import ProgressiveIcon
from ..shared.needs_character_mixin import NeedsConstants
from ..shared.touchable_mixin import TouchableMixin

from ..resource_list import Resources

from ...models.dice import Dice, roll
from ..shared.box_sized_mixin import BoxSized
from ..shared.progressive_icon import ProgressiveText
from kivymd.uix.boxlayout import MDBoxLayout
from ...models.game import THE_GAME
import typing as T

class CHDeathFails(ProgressiveIcon, NeedsConstants, TouchableMixin):
    def __init__(self, **kwargs):
        super().__init__(
            box_width=2 / 3,
            box_height=self.box_height,
            source=Resources.DEATH_FAIL,
            stacked=True,
            current_value=0,
            maximum_value=1,
            pr_empty_color="black",
            pr_full_color="darkred",
            orientation="horizontal",
        )
        self.constants_init()
        self.touch_init()

    def adapt_to_constants(self, *args):
        super().adapt_to_constants(*args)
        self.current_value = self.constants.CURRENT_DEATH_FAILS
        self.maximum_value = self.constants.MAX_DEATH_FAILS

    def on_left_click(self, *args):
        super().on_left_click(*args)
        if self.constants.CURRENT_HP <= 0:
            new_value = min(self.maximum_value, self.current_value + 1)
            THE_GAME.adjust_current_character(
                CURRENT_DEATH_FAILS=new_value,
            )

    def on_right_click(self, *args):
        super().on_right_click(*args)
        new_value = max(0, self.current_value - 1)
        THE_GAME.adjust_current_character(
            CURRENT_DEATH_FAILS=new_value,
        )


class CHDeathSuccesses(ProgressiveIcon, NeedsConstants, TouchableMixin):
    def __init__(self, **kwargs):
        super().__init__(
            box_width=2 / 3,
            box_height=self.box_height,
            source=Resources.DEATH_SUCCESS,
            stacked=True,
            current_value=0,
            maximum_value=1,
            pr_empty_color="black",
            pr_full_color="green",
            orientation="horizontal",
        )
        self.constants_init()
        self.touch_init()

    def adapt_to_constants(self, *args):
        super().adapt_to_constants(*args)
        self.current_value = self.constants.CURRENT_DEATH_SUCCESS
        self.maximum_value = self.constants.MAX_DEATH_SUCCESS

    def on_left_click(self, *args):
        super().on_left_click(*args)
        if self.constants.CURRENT_HP <= 0:
            new_value = min(self.maximum_value, self.current_value + 1)
            THE_GAME.adjust_current_character(
                CURRENT_DEATH_SUCCESS=new_value,
            )

    def on_right_click(self, *args):
        super().on_right_click(*args)
        new_value = max(0, self.current_value - 1)
        THE_GAME.adjust_current_character(
            CURRENT_DEATH_SUCCESS=new_value,
        )


class CHDeathKnockedOut(ProgressiveIcon, NeedsConstants, TouchableMixin):
    def __init__(self, **kwargs):
        super().__init__(
            box_width=2 / 3,
            box_height=self.box_height,
            source=Resources.DEATH_ICON,
            stacked=False,
            current_value=0,
            maximum_value=1,
            pr_empty_color="black",
            pr_full_color="red",
            orientation="horizontal",
        )
        self.constants_init()
        self.touch_init()

    def adapt_to_constants(self, *args):
        super().adapt_to_constants(*args)
        self.current_value = 1 if self.constants.CURRENT_HP <= 0 else 0
        self.tooltip_text = self.help_text.DEATH

    def log_for_dice_roll(self, total: int, raw: T.List[int]) -> str:
        if total == 20:
            return (
                f"Critical Success! {self.constants.CHARACTER_NAME} "
                f"is back in action."
            )
        elif total == 1:
            return (
                f"Critical failure. {self.constants.CHARACTER_NAME} "
                f"takes {self.constants.PRONOUN_HER} last breath."
            )
        elif total <= 10:
            return (f"Failure - death looms closer.")
        else:
            return "Success."

    def on_left_click(self, position):
        super().on_left_click(position)
        if self.constants.CURRENT_HP <= 0:
            result, _ = roll(
                Dice.D20,
                description=(
                    f"{self.constants.CHARACTER_NAME} is on death's door - "
                    f"{self.constants.PRONOUN_SHE} rolls a death saving throw"
                ),
                roll_type=RollStatus.STANDARD,
                post_roll_desc=self.log_for_dice_roll,
            )
            if result == 20:
                THE_GAME.adjust_current_character(
                    CURRENT_HP=1,
                    CURRENT_DEATH_SUCCESS=0,
                    CURRENT_DEATH_FAILS=0,
                )
            elif result == 1:
                THE_GAME.adjust_current_character(
                    CURRENT_DEATH_SUCCESS=0,
                    CURRENT_DEATH_FAILS=self.constants.MAX_DEATH_FAILS,
                )
            elif result <= 10:
                THE_GAME.adjust_current_character(
                    CURRENT_DEATH_FAILS=min(self.constants.CURRENT_DEATH_FAILS+1, self.constants.MAX_DEATH_FAILS),
                )
            else:
                THE_GAME.adjust_current_character(
                    CURRENT_DEATH_SUCCESS=min(self.constants.CURRENT_DEATH_SUCCESS+1, self.constants.MAX_DEATH_SUCCESS),
                )


            


class CHDeathSaves(MDBoxLayout, BoxSized, NeedsConstants):
    """
    Death Throw successes + failures
    """

    def __init__(self, **kwargs):
        super().__init__(box_width=2, box_height=1, **kwargs)
        self.box_init()
        self.constants_init()

        self.failures = CHDeathFails()
        self.successes = CHDeathSuccesses()
        self.knocked_out = CHDeathKnockedOut()

        self.add_widget(self.failures)
        self.add_widget(self.knocked_out)
        self.add_widget(self.successes)


class CHHitpoints(ProgressiveText, NeedsConstants, TouchableMixin):
    """
    Hitpoint heart
    """

    def __init__(self, **kwargs):
        super().__init__(
            source=Resources.HITPOINTS_ICON,
            pr_full_color="red",
            pr_empty_color="black",
            theme_text_color="Custom",
            text_color="white",
            current_value=0,
            maximum_value=1,
            box_width=2,
            box_height=2,
            **kwargs,
        )
        self.constants_init()
        self.touch_init()

    def adapt_to_constants(self, *args):
        super().adapt_to_constants(*args)

        self.tooltip_text = self.help_text.HP
        self.current_value = self.constants.CURRENT_HP
        self.maximum_value = self.constants.MAX_HP

    def on_left_click(self, pos):
        new_value = max(0, self.current_value - 1)
        THE_GAME.adjust_current_character(
            CURRENT_HP=new_value,
        )

    def on_right_click(self, pos):
        new_value = min(self.maximum_value, self.current_value + 1)
        THE_GAME.adjust_current_character(
            CURRENT_HP=new_value,
            CURRENT_DEATH_FAILS=0,
            CURRENT_DEATH_SUCCESS=0,
        )


class CHLife(MDBoxLayout, BoxSized, NeedsConstants):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", box_width=2, box_height=3, **kwargs)
        self.box_init()
        self.constants_init()

        self.death_saves = CHDeathSaves()
        self.hitpoints = CHHitpoints()
        self.add_widget(self.hitpoints)
        self.add_widget(self.death_saves)
