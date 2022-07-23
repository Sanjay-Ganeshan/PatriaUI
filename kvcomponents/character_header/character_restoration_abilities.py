from kivymd.uix.boxlayout import MDBoxLayout
from ..shared.box_sized_mixin import BoxSized
from ..shared.needs_character_mixin import NeedsConstants
from ..shared.progressive_icon import ProgressiveIcon
from ..shared.touchable_mixin import TouchableMixin
from ..resource_list import Resources

from ...models.dice import Dice, roll
from ...models.game import THE_GAME

class CHDeflections(ProgressiveIcon, TouchableMixin, NeedsConstants):
    def __init__(self, **kwargs):
        super().__init__(
            box_width=2,
            box_height=1,
            source=Resources.DEFLECTION,
            stacked=True,
            current_value=0,
            maximum_value=1,
            pr_empty_color="black",
            pr_full_color="blue",
            orientation="horizontal",
            **kwargs,
        )
        self.touch_init()
        self.constants_init()

    def on_left_click(self, *args):
        super().on_left_click(*args)
        new_value = max(0, self.current_value - 1)
        THE_GAME.adjust_current_character(
            CURRENT_DEFLECTS=new_value,
        )

    def on_right_click(self, *args):
        super().on_right_click(*args)
        new_value = min(self.current_value + 1, self.maximum_value)
        THE_GAME.adjust_current_character(
            CURRENT_DEFLECTS=new_value,
        )

    def adapt_to_constants(self, *args):
        super().adapt_to_constants(*args)

        self.tooltip_text = self.help_text.DEFLECT

        self.current_value = self.constants.CURRENT_DEFLECTS
        self.maximum_value = self.constants.MAX_DEFLECTS

class CHRevivals(ProgressiveIcon, TouchableMixin, NeedsConstants):
    def __init__(self, **kwargs):
        super().__init__(
            box_width=2,
            box_height=1,
            source=Resources.REVIVAL,
            stacked=True,
            current_value=0,
            maximum_value=1,
            pr_empty_color="black",
            pr_full_color="green",
            orientation="horizontal",
            **kwargs,
        )
        self.touch_init()
        self.constants_init()

    def on_left_click(self, *args):
        super().on_left_click(*args)
        if self.current_value > 0 and self.constants.CURRENT_HP <= 0:
            new_value = max(0, self.current_value - 1)
            THE_GAME.adjust_current_character(
                CURRENT_REVIVES=new_value,
                CURRENT_HP=max(1, self.constants.CURRENT_HP),
                CURRENT_DEATH_FAILS=0,
                CURRENT_DEATH_SUCCESS=0,
            )
            THE_GAME.game_log.log(f"{self.constants.CHARACTER_NAME} gets back up. [RClick HP to correct amount]")

    def on_right_click(self, *args):
        super().on_right_click(*args)
        new_value = min(self.current_value + 1, self.maximum_value)
        THE_GAME.adjust_current_character(
            CURRENT_REVIVES=new_value,
        )
    
    def adapt_to_constants(self, *args):
        super().adapt_to_constants(*args)

        self.tooltip_text = self.help_text.REVIVAL

        self.current_value = self.constants.CURRENT_REVIVES
        self.maximum_value = self.constants.MAX_REVIVES

class CHHitDice(ProgressiveIcon, TouchableMixin, NeedsConstants):
    def __init__(self, **kwargs):
        super().__init__(
            box_width=2,
            box_height=1,
            source=Resources.HIT_DICE,
            stacked=True,
            current_value=0,
            maximum_value=1,
            pr_empty_color="black",
            pr_full_color="red",
            orientation="horizontal",
            **kwargs,
        )
        self.touch_init()
        self.constants_init()

    def on_left_click(self, *args):
        super().on_left_click(*args)
        if self.current_value > 0 and self.constants.CURRENT_HP < self.constants.MAX_HP:
            new_value = max(0, self.current_value - 1)
            regen, _ = roll(
                Dice.D6,
                description=f"{self.constants.CHARACTER_NAME} regenerates using hit dice"
            )
            new_hp = min(self.constants.CURRENT_HP + regen, self.constants.MAX_HP)
            THE_GAME.adjust_current_character(
                CURRENT_HIT_DICE=new_value,
                CURRENT_HP=new_hp
            )

    def on_right_click(self, *args):
        super().on_right_click(*args)
        new_value = min(self.current_value + 1, self.maximum_value)
        THE_GAME.adjust_current_character(
            CURRENT_HIT_DICE=new_value,
        )
    
    def adapt_to_constants(self, *args):
        super().adapt_to_constants(*args)

        self.tooltip_text = self.help_text.HIT_DICE

        self.current_value = self.constants.CURRENT_HIT_DICE
        self.maximum_value = self.constants.MAX_HIT_DICE

    

class CHRestoration(MDBoxLayout, BoxSized, NeedsConstants):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", box_width=2, box_height=3, **kwargs)
        self.box_init()
        self.constants_init()

        self.deflections = CHDeflections()

        self.revivals = CHRevivals()

        self.hit_dice = CHHitDice()

        self.add_widget(self.deflections)
        self.add_widget(self.revivals)
        self.add_widget(self.hit_dice)
