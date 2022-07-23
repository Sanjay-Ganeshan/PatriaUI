from kivymd.uix.boxlayout import MDBoxLayout
from ..shared.box_sized_mixin import BoxSized
from ..shared.needs_character_mixin import NeedsConstants
from ..shared.progressive_icon import ProgressiveIconImpl, AnyIcon
from ..shared.centered_label import CenteredLabel
from ..shared.touchable_mixin import TouchableMixin
from kivy.properties import (
    StringProperty,
    NumericProperty,
    StringProperty,
)
from ..shared.spacer import Spacer
from ...models.character import Constants
from ...models.game import THE_GAME
from ...models.dice import Dice, RollStatus, roll

from ..resource_list import Resources
import typing as T


class SkillTag(MDBoxLayout, BoxSized, NeedsConstants, ProgressiveIconImpl, TouchableMixin):
    skill_name = StringProperty("FILLME")
    proficiency_multiplier = NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__(
            box_width=2,
            box_height=1,
            source=Resources.SKILL_TAG_BASIC,
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
        self.constants_init()
        self.touch_init()

        self.space = Spacer(box_width=0.3, box_height=1)
        self.add_widget(self.space)

        self.skill_icon = AnyIcon(
            source=Resources.ENERGY_SHIELD_ICON,
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
            skill_name=self.on_prof_changed, proficiency_multiplier=self.on_prof_changed
        )

        self.on_prof_changed()

    def _get_label_string(self) -> str:
        total_bonus = self._get_total_bonus()
        real_skill_name = self._get_real_skill_name()
        return f"{real_skill_name}:\n{total_bonus:+d}"

    def _get_total_bonus(self) -> int:
        stat_mod, proficiency_bonus = self._get_stat_mod_and_proficiency_bonus()
        return stat_mod + self.proficiency_multiplier * proficiency_bonus

    def _get_stat_name(self) -> str:
        return Constants.expand_stat_abbreviation(self.skill_name.split("_")[0])

    def _get_stat_mod_and_proficiency_bonus(self) -> T.Tuple[int, int]:
        proficiency_bonus = (
            0 if self.constants is None else self.constants.S_PROFICIENCY_BONUS
        )
        my_stat = self._get_stat_name()
        stat_mod = (
            0 if self.constants is None else getattr(self.constants, f"S_{my_stat}")
        )

        return stat_mod, proficiency_bonus

    def _get_real_skill_name(self) -> str:
        return " ".join(self.skill_name.split("_")[1:])

    def _get_help_text(self) -> str:
        skill_desc = self.help_text.SKILL_DESCRIPTIONS[self.skill_name]
        stat_mod, proficiency_bonus = self._get_stat_mod_and_proficiency_bonus()
        total_bonus = self._get_total_bonus()
        real_skill_name = self._get_real_skill_name()

        if self.proficiency_multiplier == 0:
            general_desc = (
                f"You have no additional bonuses past your "
                f"stat modifier ({stat_mod:+d})."
            )
        elif self.proficiency_multiplier == 1:
            general_desc = (
                f"You are proficient in {real_skill_name}.\n"
                f"Add your proficiency bonus ({proficiency_bonus:+d}) to rolls,\n"
                f"in addition to your stat modifier ({stat_mod:+d})\n"
                f"Total: {total_bonus:+d}"
            )
        elif self.proficiency_multiplier == 2:
            general_desc = (
                f"You are proficient in {real_skill_name}.\n"
                f"Add DOUBLE your proficiency bonus ({2*proficiency_bonus:+d}) to rolls,\n"
                f"in addition to your stat modifier ({stat_mod:+d})\n"
                f"Total: {total_bonus:+d}"
            )
        else:
            raise ValueError(
                f"Bad proficiency in {self.skill_name} -- {self.proficiency_multiplier}"
            )

        return f"{skill_desc}\n{general_desc}"

    def _get_bg_icon(self) -> str:
        if self.proficiency_multiplier == 0:
            return Resources.SKILL_TAG_BASIC
        elif self.proficiency_multiplier == 1:
            return Resources.SKILL_TAG_PROFICIENT
        elif self.proficiency_multiplier == 2:
            return Resources.SKILL_TAG_EXPERT
        else:
            raise ValueError(
                f"Bad proficiency in {self.skill_name} -- {self.proficiency_multiplier}"
            )

    def _get_icon_and_color(self) -> T.Tuple[str, T.Any]:
        color = ["black", "white", "gold"][self.proficiency_multiplier]
        icon = Resources.SKILL_ICONS.get(self.skill_name, Resources.DEATH_FAIL)
        return icon, color

    def on_prof_changed(self, *args):
        self.skill_name_label.text = self._get_label_string()
        self.skill_icon.tooltip_text = self._get_help_text()
        self.source = self._get_bg_icon()

        (
            self.skill_icon.source,
            self.skill_icon.pr_full_color,
        ) = self._get_icon_and_color()

    def adapt_to_constants(self, *args):
        super().adapt_to_constants(*args)

        self.proficiency_multiplier = getattr(self.constants, f"P_{self.skill_name}")


    def on_left_click(self, *args):
        super().on_left_click(*args)
        roll(
            Dice.D20,
            description=(
                f"{self.constants.CHARACTER_NAME} tests {self._get_real_skill_name()}"
            ),
            modifier=self._get_total_bonus()
        )

    def on_right_click(self, *args):
        super().on_right_click(*args)