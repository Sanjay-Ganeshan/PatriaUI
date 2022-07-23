from ..shared.progressive_icon import ProgressiveIcon
from ..shared.needs_character_mixin import NeedsConstants
from ..shared.touchable_mixin import TouchableMixin

from ..resource_list import Resources

from ...models.dice import Dice, roll
from ..shared.box_sized_mixin import BoxSized
from ..shared.progressive_icon import ProgressiveText
from kivymd.uix.boxlayout import MDBoxLayout
from ...models.game import THE_GAME


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
            pr_full_color="darkgreen",
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

    def on_left_click(self, position):
        super().on_left_click(position)
        if self.constants.CURRENT_HP <= 0:
            result, _ = roll(
                Dice.D20,
                description=(
                    f"{self.constants.CHARACTER_NAME} is on death's door - "
                    f"{self.constants.PRONOUN_SHE} rolls a death saving throw"
                ),
            )

            if result == 20:
                THE_GAME.game_log.log(
                    f"Critical Success! {self.constants.CHARACTER_NAME} "
                    f"is back in action."
                )
            elif result == 1:
                THE_GAME.game_log.log(
                    f"Critical failure. {self.constants.CHARACTER_NAME} "
                    f"takes {self.constants.PRONOUN_HER} last breath."
                )
            elif result <= 10:
                THE_GAME.game_log.log(f"Failure - death looms closer.")
            else:
                THE_GAME.game_log.log("")


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
