import typing as T

from kivy.properties import NumericProperty, ObjectProperty
from kivymd.uix.boxlayout import MDBoxLayout

from ...new_models.character.character import Character
from ...new_models.character.proficiencies import Proficiency
from ...new_models.character.stats import Stat
from ...new_models.events.ev_base import GameOrViewEvent
from ...new_models.events.game_events import StatOrSkillTest
from ...new_models.help import help_generator
from ...new_models.state.state_manager import StateManager
from ..resource_list import Resources
from ..shared.box_sized_mixin import BoxSized
from ..shared.centered_label import CenteredLabel
from ..shared.listens_for_state_changes import ListenForStateChanges
from ..shared.progressive_icon import AnyIcon, ProgressiveIconImpl
from ..shared.spacer import Spacer
from ..shared.touchable_mixin import TouchableMixin


class SkillTag(
    MDBoxLayout, BoxSized, ListenForStateChanges, ProgressiveIconImpl, TouchableMixin
):
    which_skill: Proficiency = ObjectProperty(Proficiency.ACROBATICS)
    proficiency_multiplier: int = NumericProperty(0)

    stat_bonus: int = NumericProperty(0)
    proficiency_bonus: int = NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__(
            box_width=2,
            box_height=1,
            source=Resources.PROFICIENCY_MULTIPLIER_TO_SKILL_TAG[0],
            current_value=1,
            maximum_value=1,
            stacked=False,
            orientation="horizontal",
            pr_full_color=kwargs.pop("pr_full_color", "white"),
            pr_empty_color="black",
            **kwargs,
        )
        self.progressive_init()
        self.box_init()
        self.listener_init()
        self.touch_init()

        self.space = Spacer(box_width=0.3, box_height=1)
        self.add_widget(self.space)

        self.skill_icon = AnyIcon(
            source=Resources.MISSING,
            pr_full_color="gold",
            box_width=0.4,
            box_height=1.0,
        )

        self.skill_name_label = CenteredLabel(
            text="",
            font_style="H6",
            tooltip_text="",
            box_width=1.3,
            box_height=1.0,
        )

        self.add_widget(self.skill_icon)
        self.add_widget(self.skill_name_label)

        self.bind(
            which_skill=self.on_prof_changed,
            proficiency_multiplier=self.on_prof_changed,
            stat_bonus=self.on_prof_changed,
            proficiency_bonus=self.on_prof_changed,
        )

        self.on_prof_changed()

    def _get_total_bonus(self) -> int:
        return self.stat_bonus + self.proficiency_multiplier * self.proficiency_bonus

    def on_prof_changed(self, *args):
        self.skill_name_label.text = (
            f"{self.which_skill.value}:\n{self._get_total_bonus():+d}"
        )
        self.skill_icon.tooltip_text = help_generator.skill_description(
            self.which_skill,
            multiplier=self.proficiency_multiplier,
            stat_mod=self.stat_bonus,
            proficiency_bonus=self.proficiency_bonus,
            total_bonus=self._get_total_bonus(),
        )
        prof_idx = max(0, min(2, self.proficiency_multiplier))
        self.source = Resources.PROFICIENCY_MULTIPLIER_TO_SKILL_TAG[prof_idx]
        self.skill_icon.pr_full_color = ["black", "white", "gold"][prof_idx]
        self.skill_icon.source = Resources.SKILL_TO_ICON.get(
            self.which_skill, Resources.MISSING
        )

    def listener(
        self, ev: GameOrViewEvent, is_forward: bool, state_manager: StateManager
    ) -> None:
        # No reason to filter events, kivy will figure things out when we set properties

        # We might have changed the current character's icon. Look it up
        if state_manager.view_state.focused_character is None:
            self.proficiency_multiplier = 0
            self.proficiency_bonus = 0
            self.stat_bonus = 0
        else:
            char: Character = state_manager.game_state.characters[
                state_manager.view_state.focused_character
            ]
            self.proficiency_multiplier = char.stat_block[self.which_skill]
            self.stat_bonus = char.stat_block[self.which_skill.corresponding_stat()]
            self.proficiency_bonus = char.stat_block[Stat.PROFICIENCY_BONUS]

    def on_left_click(self, *args):
        super().on_left_click(*args)

        if self.state_manager is None:
            return

        if self.state_manager.view_state.focused_character is None:
            return

        # Left click -> Cast Reactive Armor
        self.state_manager.push_event(
            StatOrSkillTest(
                character_id=self.state_manager.view_state.focused_character,
                stat_or_skill=self.which_skill,
            )
        )

    def on_right_click(self, *args):
        super().on_right_click(*args)
