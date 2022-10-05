from kivymd.uix.boxlayout import MDBoxLayout

from ..shared.box_sized_mixin import BoxSized
from ..shared.progressive_icon import ProgressiveIcon
from ..shared.touchable_mixin import TouchableMixin
from ..resource_list import Resources

from ..shared.listens_for_state_changes import ListenForStateChanges
from ...new_models.help import help_generator
from ...new_models.events.ev_base import GameOrViewEvent
from ...new_models.events.game_events import CastDeflect, RestoreDeflect, ConsumeRevival, RestoreRevival, RestoreHitDice, UseHitDice
from ...new_models.state.state_manager import StateManager
from ...new_models.character.character import Character
from ...new_models.character.status import Status
from ...new_models.character.stats import Stat
from kivy.properties import NumericProperty

class CHDeflections(ProgressiveIcon, TouchableMixin, ListenForStateChanges):
    current_deflects: int = NumericProperty(1)
    max_deflects: int = NumericProperty(1)
    int_modifier: int = NumericProperty(1)

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
        self.listener_init()

        self.bind(current_deflects=self.update_deflects, max_deflects=self.update_deflects)

    def listener(
        self, ev: GameOrViewEvent, is_forward: bool, state_manager: StateManager
    ) -> None:
        # No reason to filter events, kivy will figure things out when we set properties

        if state_manager.view_state.focused_character is None:
            self.current_death_fails = 0
            self.max_death_fails = 1
        else:
            char: Character = state_manager.game_state.characters[
                state_manager.view_state.focused_character
            ]
            current: Status = char.current_life
            maxi: Status = char.max_life

            self.current_deflects = current.deflects
            self.max_deflects = maxi.deflects
            self.int_modifier = char.stat_block[Stat.INTELLIGENCE]

    def on_left_click(self, *args):
        super().on_left_click(*args)
        if self.state_manager is None:
            return
        if self.state_manager.view_state.focused_character is None:
            return
        
        char_id: str = self.state_manager.view_state.focused_character
        self.state_manager.push_event(CastDeflect(character_id=char_id))

    def on_right_click(self, *args):
        super().on_right_click(*args)
        if self.state_manager is None:
            return
        if self.state_manager.view_state.focused_character is None:
            return
        
        char_id: str = self.state_manager.view_state.focused_character
        self.state_manager.push_event(RestoreDeflect(character_id=char_id))

    def update_deflects(self, *args):
        self.tooltip_text = help_generator.deflect(n_free_casts=self.current_deflects, max_free_casts=self.max_deflects, intelligence=self.int_modifier)

        self.current_value = self.current_deflects
        self.maximum_value = self.max_deflects

class CHRevivals(ProgressiveIcon, TouchableMixin, ListenForStateChanges):
    current_revives: int = NumericProperty(1)
    max_revives: int = NumericProperty(1)

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
        self.listener_init()

        self.bind(current_revives=self.revives_updated, max_revives=self.revives_updated)

    def on_left_click(self, *args):
        super().on_left_click(*args)
        if self.state_manager is None:
            return
        if self.state_manager.view_state.focused_character is None:
            return
        
        char_id: str = self.state_manager.view_state.focused_character
        self.state_manager.push_event(ConsumeRevival(character_id=char_id))

    def on_right_click(self, *args):
        super().on_right_click(*args)
        if self.state_manager is None:
            return
        if self.state_manager.view_state.focused_character is None:
            return
        
        char_id: str = self.state_manager.view_state.focused_character
        self.state_manager.push_event(RestoreRevival(character_id=char_id))
    
    def revives_updated(self, *args):
        self.tooltip_text = help_generator.revive(self.current_revives, self.max_revives)

        self.current_value = self.current_revives
        self.maximum_value = self.max_revives

    def listener(
        self, ev: GameOrViewEvent, is_forward: bool, state_manager: StateManager
    ) -> None:
        # No reason to filter events, kivy will figure things out when we set properties

        if state_manager.view_state.focused_character is None:
            self.current_revives = 1
            self.max_revives = 1
        else:
            char: Character = state_manager.game_state.characters[
                state_manager.view_state.focused_character
            ]
            self.current_revives = char.current_life.revives
            self.max_revives = char.max_life.revives

class CHHitDice(ProgressiveIcon, TouchableMixin, ListenForStateChanges):
    current_hit_dice: int = NumericProperty(1)
    max_hit_dice: int = NumericProperty(1)

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
            tooltip_text=help_generator.hit_dice(),
            **kwargs,
        )
        self.touch_init()
        self.listener_init()

        self.bind(current_hit_dice=self.update_hit_dice, max_hit_dice=self.update_hit_dice)

    def listener(
        self, ev: GameOrViewEvent, is_forward: bool, state_manager: StateManager
    ) -> None:
        # No reason to filter events, kivy will figure things out when we set properties

        if state_manager.view_state.focused_character is None:
            self.current_hit_dice = 1
            self.max_hit_dice = 1
        else:
            char: Character = state_manager.game_state.characters[
                state_manager.view_state.focused_character
            ]
            self.current_hit_dice = char.current_life.hit_dice
            self.max_hit_dice = char.max_life.hit_dice


    def on_left_click(self, *args):
        super().on_left_click(*args)
        if self.state_manager is None:
            return
        if self.state_manager.view_state.focused_character is None:
            return
        
        char_id: str = self.state_manager.view_state.focused_character
        self.state_manager.push_event(UseHitDice(character_id=char_id))

    def on_right_click(self, *args):
        super().on_right_click(*args)
        if self.state_manager is None:
            return
        if self.state_manager.view_state.focused_character is None:
            return
        
        char_id: str = self.state_manager.view_state.focused_character
        self.state_manager.push_event(RestoreHitDice(character_id=char_id))
    
    def update_hit_dice(self, *args):
        self.current_value = self.current_hit_dice
        self.maximum_value = self.max_hit_dice

    

class CHRestoration(MDBoxLayout, BoxSized, ListenForStateChanges):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", box_width=2, box_height=3, **kwargs)
        self.box_init()
        self.listener_init()

        self.deflections = CHDeflections()

        self.revivals = CHRevivals()

        self.hit_dice = CHHitDice()

        self.add_widget(self.deflections)
        self.add_widget(self.revivals)
        self.add_widget(self.hit_dice)
