from kivy.uix.image import Image
from kivymd.uix.boxlayout import MDBoxLayout

from ...new_models.character.character import Character

from ...new_models.state.app_settings import BOX_WIDTH, BOX_HEIGHT
from ..shared.box_sized_mixin import BoxSized
from ..shared.touchable_mixin import TouchableMixin
from ..shared.tooltip import OptionalTooltip
from ..shared.listens_for_state_changes import ListenForStateChanges
from ..resource_list import Resources
from ...new_models.state.state_manager import StateManager
from ...new_models.events.ev_base import GameOrViewEvent
from ...new_models.spells.spell_list import Spell
from ...new_models.events.abilities import cast_spell, followup_spell
from ...new_models.help import help_generator
from ...new_models.character.stats import Stat
import typing as T
from kivy.properties import ObjectProperty, NumericProperty


class SpellIcon(
    Image, BoxSized, ListenForStateChanges, TouchableMixin, OptionalTooltip
):
    which_spell = ObjectProperty(Spell.INCINERATE)

    spell_save_dc = NumericProperty(11)
    spell_attack_bonus = NumericProperty(0)
    int_modifier = NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__(
            source="",
            allow_stretch=True,
            **kwargs,
        )

        self.box_init()
        self.touch_init()
        self.listener_init()

        self.bind(
            which_spell=self.spell_changed,
            spell_save_dc=self.spell_changed,
            spell_attack_bonus=self.spell_changed,
            int_modifier=self.spell_changed
        )
        self.spell_changed()

    def spell_changed(self, *args):
        self.source = Resources.SPELLS[self.which_spell]
        self.color = Resources.SPELL_COLORS[self.which_spell]
        self.tooltip_text = help_generator.spell_description(
            which_spell=self.which_spell,
            spell_save_dc=self.spell_save_dc,
            spell_attack_bonus=self.spell_attack_bonus,
            intelligence=self.int_modifier,
        )

    def listener(
        self, ev: GameOrViewEvent, is_forward: bool, state_manager: StateManager
    ) -> None:
        if state_manager.view_state.focused_character is None:
            self.spell_save_dc = 11
            self.spell_attack_bonus = 0
            self.int_modifier = 0
        else:
            char: Character = state_manager.game_state.characters[
                state_manager.view_state.focused_character]
            self.spell_save_dc = 11 + char.stat_block[
                Stat.PROFICIENCY_BONUS] + char.stat_block[Stat.INTELLIGENCE]
            self.int_modifier = char.stat_block[Stat.INTELLIGENCE]
            self.spell_attack_bonus = char.stat_block[
                Stat.PROFICIENCY_BONUS] + char.stat_block[Stat.INTELLIGENCE]

    def on_left_click(self, position):
        super().on_left_click(position)
        if self.state_manager is None:
            return

        if self.state_manager.view_state.focused_character is None:
            return

        self.state_manager.push_event(
            cast_spell(
                character_id=self.state_manager.view_state.focused_character,
                which_spell=self.which_spell
            )
        )

    def on_right_click(self, position):
        super().on_right_click(position)
        if self.state_manager is None:
            return

        if self.state_manager.view_state.focused_character is None:
            return

        self.state_manager.push_event(
            followup_spell(
                character_id=self.state_manager.view_state.focused_character,
                which_spell=self.which_spell
            )
        )


class SpellBar(BoxSized, MDBoxLayout, ListenForStateChanges):
    def __init__(self, **kwargs):
        super().__init__(
            box_width=BOX_WIDTH,
            box_height=2,
            orientation="horizontal",
        )
        self.box_init()
        self.listener_init()

        self.spells: T.Dict[Spell, SpellIcon] = {}
        for each_spell in Spell.all():
            self.spells[each_spell] = SpellIcon(
                which_spell=each_spell,
                box_width=1.5,
                box_height=2,
            )

        # Spell.all() is ordered
        for each_spell in Spell.all():
            self.add_widget(self.spells[each_spell])
