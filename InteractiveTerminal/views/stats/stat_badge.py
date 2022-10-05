from kivy.properties import NumericProperty, ObjectProperty

from ...new_models.character.character import Character
from ...new_models.character.stats import Stat
from ...new_models.events.ev_base import GameOrViewEvent
from ...new_models.events.game_events import StatOrSkillTest
from ...new_models.help import help_generator
from ...new_models.state.state_manager import StateManager
from ..resource_list import Resources
from ..shared.centered_label import CenteredLabel
from ..shared.listens_for_state_changes import ListenForStateChanges
from ..shared.progressive_icon import ProgressiveIconImpl
from ..shared.touchable_mixin import TouchableMixin


class StatBadge(
    CenteredLabel, ProgressiveIconImpl, ListenForStateChanges, TouchableMixin
):
    """
    A box displaying a single stat
    """

    which_stat = ObjectProperty(Stat.PROFICIENCY_BONUS)
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
        self.touch_init()
        self.listener_init()

        self.bind(which_stat=self.on_stats_changed, stat_modifier=self.on_stats_changed)
        self.on_stats_changed()

    def on_stats_changed(self, *args):
        self.text = self.which_stat.value + "\n" + ("%+d" % self.stat_modifier)
        self.tooltip_text = help_generator.stat_description(
            self.which_stat, self.stat_modifier
        )

    def listener(
        self, ev: GameOrViewEvent, is_forward: bool, state_manager: StateManager
    ) -> None:
        # No reason to filter events, kivy will figure things out when we set properties

        # We might have changed the current character's icon. Look it up
        if state_manager.view_state.focused_character is None:
            self.stat_modifier = 0
        else:
            char: Character = state_manager.game_state.characters[
                state_manager.view_state.focused_character
            ]
            self.stat_modifier = char.stat_block[self.which_stat]

    def on_left_click(self, *args):
        super().on_left_click(*args)

        if self.which_stat == Stat.PROFICIENCY_BONUS:
            # Can't roll "proficiency", gotta roll a particular skill
            return

        if self.state_manager is None:
            return

        if self.state_manager.view_state.focused_character is None:
            return

        # Left click -> Cast Reactive Armor
        self.state_manager.push_event(
            StatOrSkillTest(
                character_id=self.state_manager.view_state.focused_character,
                stat_or_skill=self.which_stat,
            )
        )
